from app.services import ProjectGetter

from .cache import Cache


def get_projecten() -> ProjectGetter:
    return ProjectGetter()


class Store:
    activiteiten_current = Cache[ProjectGetter](getter=get_projecten)


store = Store()

__all__ = ["store"]
