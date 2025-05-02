import asyncio
import math
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Tuple

import aiohttp
import numpy as np


@dataclass
class ResponseDetail:
    status_code: int
    request_start: str
    request_end: str
    response_time: float


@dataclass
class ResponseStatistics:
    requests_per_sec: float
    duration: float
    n_requests: int
    avg: float
    percentile_50: float
    percentile_90: float
    percentile_99: float


@dataclass
class RequestBatch:
    urls: list[str]
    requests_per_second: float
    duration_seconds: int

    def __post_init__(self):
        self.responses: None | list[ResponseDetail] = None

    async def perform_requests(self):
        n_requests = math.ceil(self.duration_seconds * self.requests_per_second)
        if n_requests > len(self.urls):
            n_repeat = math.ceil(n_requests / len(self.urls))
            full_url_list = self.urls * n_repeat
        else:
            full_url_list = self.urls

        full_url_list = full_url_list[:n_requests]

        sleep_duration = self.duration_seconds / n_requests
        tasks = [
            self.fetch_url_async(url, sleep=index * sleep_duration)
            for (index, url) in enumerate(full_url_list)
        ]
        responses: list[ResponseDetail] = await asyncio.gather(*tasks)
        self.responses = responses

    @property
    def responses_ok(self) -> list[ResponseDetail] | None:
        if self.responses is not None:
            return [
                r
                for r in self.responses
                if r.status_code >= 200 and r.status_code < 300
            ]
        else:
            raise ValueError("No response with status code 200 received")

    @property
    def statistics(self) -> ResponseStatistics | None:
        if self.responses:
            response_times = [r.response_time for r in self.responses]
            return ResponseStatistics(
                **{
                    "requests_per_sec": self.requests_per_second,
                    "duration": self.duration_seconds,
                    "n_requests": len(response_times),
                    "avg": sum(response_times) / len(response_times),
                    "percentile_50": np.percentile(np.array(response_times), 50),
                    "percentile_90": np.percentile(np.array(response_times), 90),
                    "percentile_99": np.percentile(np.array(response_times), 90),
                }
            )

    @staticmethod
    async def fetch_url_async(url: str, sleep: float | None = None) -> ResponseDetail:
        if sleep is not None:
            await asyncio.sleep(sleep)
        request_start = datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                request_end = datetime.now()
                duration = (request_end - request_start).total_seconds()  # seconds
                time_format = "%Y-%m-%d, %H:%M:%S"
                response_detail = ResponseDetail(
                    **{
                        "status_code": response.status,
                        "request_start": request_start.strftime(time_format),
                        "request_end": request_end.strftime(time_format),
                        "response_time": duration,  # seconds
                    }
                )
                return response_detail


Locations = Literal["below target", "above target", "within target"]


@dataclass
class PerformanceIterator:
    target_response_time_percentile_90: float  # seconds
    duration_seconds: int
    urls: list[str]
    request_per_sec_initial: int = 1

    def __post_init__(self):
        self.responses_statistics: list[ResponseStatistics] = []

    @property
    def target_min_max(self) -> Tuple[float, float]:
        margin = 0.1
        return self.target_response_time_percentile_90 * (
            1 - margin
        ), self.target_response_time_percentile_90 * (1 + margin)

    def get_response_statistics(self, location: Locations) -> ResponseStatistics | None:
        def filter_response_statistics(
            location: Locations, response_statistics: ResponseStatistics
        ):
            allow = False
            target_min = self.target_min_max[0]
            target_max = self.target_min_max[1]
            if location == "above target":
                allow = response_statistics.percentile_90 >= target_min
            elif location == "below target":
                allow = response_statistics.percentile_90 <= target_max
            elif location == "within target":
                allow = (
                    response_statistics.percentile_90 >= target_min
                    and response_statistics.percentile_90 <= target_max
                )

            return allow

        response_times_statistics = sorted(
            [
                r
                for r in self.responses_statistics
                if filter_response_statistics(location=location, response_statistics=r)
            ],
            key=lambda x: x.requests_per_sec,
            reverse=location == "below target",
        )

        if len(response_times_statistics) > 0:
            return response_times_statistics[0]

    @property
    def iteration_required(self) -> bool:
        response_times_within_targets = self.get_response_statistics(
            location="within target"
        )
        if response_times_within_targets is not None:
            s = response_times_within_targets
            print(
                f"Target reached: {s.requests_per_sec} request per second, response_time 90th percentile: {s.percentile_90}"  # noqa
            )
            return False
        else:
            return True

    async def iterate_to_target(self):
        requests_per_second_default = self.request_per_sec_initial
        while self.iteration_required:
            stats_above_target = self.get_response_statistics(location="above target")
            stats_below_target = self.get_response_statistics(location="below target")
            if stats_above_target is not None and stats_below_target is not None:
                n_requests_per_sec_upper = stats_above_target.requests_per_sec
                n_requests_per_sec_bottom = stats_below_target.requests_per_sec
                requests_per_second = (
                    n_requests_per_sec_bottom
                    + (n_requests_per_sec_upper - n_requests_per_sec_bottom) / 2
                )
            else:
                requests_per_second = requests_per_second_default
            await self.perform_request(requests_per_second=requests_per_second)
            stats_above_target = self.get_response_statistics(location="above target")
            if stats_above_target is None:
                requests_per_second_default = requests_per_second_default * 2
            elif stats_below_target is None:
                requests_per_second_default = requests_per_second_default / 2

    async def perform_request(self, requests_per_second: float):
        request_batch = RequestBatch(
            urls=self.urls,
            duration_seconds=self.duration_seconds,
            requests_per_second=requests_per_second,
        )
        await request_batch.perform_requests()
        if request_batch.statistics:
            matched_existing_statistic = [
                r
                for r in self.responses_statistics
                if r.requests_per_sec == requests_per_second
            ]
            if len(matched_existing_statistic) > 0:
                matched_existing_statistic[0] = request_batch.statistics
            else:
                self.responses_statistics.append(request_batch.statistics)

            if request_batch.statistics:
                print(request_batch.statistics)


async def main():
    base_urls = {
        "local": "http://localhost:8000",
        "tst": "https://rid-public-frontend.ictu-devops-tst.test3.s15m.nl",
    }

    base_url = base_urls["local"]

    urls = [
        f"{base_url}/api/project/?limit=10&filters=%5B%5D&sorting=%5B%7B%22attribute%22%3A%22ProjectVersieWijzigingsDatum%22%2C%22direction%22%3A%22desc%22%7D%5D",  # noqa
        f"{base_url}/api/project/?limit=20&page=1&search=pro&filters=%5B%5D&sorting=%5B%7B%22attribute%22%3A%22MinisterieNaam%22%2C%22direction%22%3A%22asc%22%7D%5D&aggregation_attributes=%5B%22MinisterieNaam%22%2C%22Onderwerp%22%2C%22ProjectStatus%22%2C%22HeeftAcICTAdvies%22%2C%22Dienstverlening%22%2C%22MaatschappelijkeBaat%22%5D",  # noqa
    ]

    iterator = PerformanceIterator(
        target_response_time_percentile_90=1,
        duration_seconds=5,
        urls=urls,
        request_per_sec_initial=2,
    )
    await iterator.iterate_to_target()

    print(iterator.get_response_statistics(location="within target"))


if __name__ == "__main__":
    asyncio.run(main())
