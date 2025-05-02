import logging
from typing import Callable, Generic, TypeVar, cast

import diskcache

from app.config.env import settings

logger = logging.getLogger("uvicorn")


T = TypeVar("T")


class Cache(Generic[T]):
    """
    Cache a value returned by a function.

    - The get method executes the getter function if no cached value is stored.
    - The update method will always run the getter function and store the result.

    Caching is performed in two steps:
    1. The getter function (which is the most expensive) stores the data to diskcache (stored in a pvc directory). This enables every pod to access this cache.
    2. This data is then stored in memory of the pod, because reading from disk takes too long (>500ms).

    """

    def __init__(self, getter: Callable, kwargs: dict | None = None):
        self.getter = getter
        self.kwargs = kwargs if kwargs else {}
        self.__cache_provider = diskcache.Cache(f"{settings.PVC_DIRECTORY}cache")
        self.__cache_key = "projecten"
        self.__memcached_value: T | None = None

    @property
    def __diskcached_value(self):
        if self.__cache_key not in self.__cache_provider:
            self.update()
        assert self.__cache_key in self.__cache_provider
        return cast(T, self.__cache_provider.get(self.__cache_key))

    def get(self):
        if not self.__memcached_value:
            self.__memcached_value = self.__diskcached_value
        return self.__memcached_value

    def set(self, data: T):
        """Store the data in the disk cache provider"""
        self.__cache_provider[self.__cache_key] = data

    def update(self):
        logger.info("Start updating cache...")
        result = self.getter(**self.kwargs)
        self.set(result)
        logger.info("Updating cache finished")
