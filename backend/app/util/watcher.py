import logging
from dataclasses import dataclass
from typing import Any, Callable

from app.config.env import settings
from app.util.timer import RepeatTimer

logger = logging.getLogger("uvicorn")

DISABLE_WACHTER_INITIALIZATION = settings.DISABLE_WACHTER_INITIALIZATION == "1"


@dataclass
class Watcher:
    """
    Watch a variable that is returned from a function.
    If the value changes, a callback is executed.

    Args:
    - watch_fn: the function used to retrieve the watched value
    - interval: time in seconds. Each interval, the watch function is executed.
    - callback: this function called when the watched value has changed
    """

    watch_fn: Callable[[], Any | None]
    callback: Callable
    interval: int

    def __post_init__(self):
        self.__watch_value = None

    def start(self):
        if not DISABLE_WACHTER_INITIALIZATION:
            self.watch()  # don't await the first interval
        self.timer = RepeatTimer(interval=self.interval, function=self.watch)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def watch(self):
        new_watch_value = self.watch_fn()

        if new_watch_value != self.__watch_value and new_watch_value is not None:
            logger.info(
                f"New watch value: {new_watch_value}, old watch value {self.__watch_value}"
            )
            self.callback()
        self.__watch_value = new_watch_value
