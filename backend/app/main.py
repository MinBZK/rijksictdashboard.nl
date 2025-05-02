import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

# from app.util.timer import RepeatTimer
from app.config.env import settings
from app.misc import init_view
from app.routers import (
    default,
    health,
    ict_kosten,
    jbr_file,
    kwiv,
    metrics,
    ministerie,
    opendata,
    text_loader,
    project,
    project_agg,
    search,
)
from app.store import store
from app.store.watch import watch

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_view.init_view()
    # start CMS watcher
    watch.start()

    # Get the activiteiten once to ensure it is cached in memory
    logger.info("Storing activititeiten in memory")
    store.activiteiten_current.get()
    yield
    watch.stop()


app = FastAPI(
    docs_url="/api-docs" if settings.SHOW_API_DOCS == "1" else None,
    title="Rijks ICT-dashboard API",
    description="Publieke backend voor het verkrijgen van informatie voor het Rijks ICT-dashboard",
    lifespan=lifespan,
)

if settings.DEPLOYMENT_ENV == "local":
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

router = APIRouter()
app.include_router(default.router)
app.include_router(project.router, prefix="/project", tags=["Project"])
app.include_router(
    project_agg.router, prefix="/project-aggregatie", tags=["Aggregatie"]
)
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(jbr_file.router, prefix="/jbr-file", tags=["JBR file"])
app.include_router(ministerie.router, prefix="/ministerie", tags=["Ministerie"])
app.include_router(ict_kosten.router, prefix="/ict-kosten", tags=["ICT-kosten"])
app.include_router(text_loader.router, tags=["text_loader"])
app.include_router(search.router, prefix="/search", tags=["Zoeken"])
app.include_router(health.router, prefix="/health", tags=["Health Check"])
app.include_router(kwiv.router, prefix="/kwiv", tags=["KWIV data"])
app.include_router(opendata.router, prefix="/opendata", tags=["Open data"])


app.mount("/api", app)
