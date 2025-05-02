from app.services import get_laatste_wijziging
from app.store import store
from app.util.watcher import Watcher

watch = Watcher(
    watch_fn=get_laatste_wijziging,
    interval=10,
    callback=store.activiteiten_current.update,
)
