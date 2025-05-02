from logging import getLogger
from threading import Timer

logger = getLogger("uvicorn")


# https://stackoverflow.com/a/48741004
class RepeatTimer(Timer):
    def exec_fn(self):
        self.function(*self.args, **self.kwargs)

    def run(self):
        while not self.finished.wait(self.interval):
            self.exec_fn()
