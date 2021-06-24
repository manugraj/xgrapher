from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger

from src.api.v1.data import router as data_route
from src.api.v1.query import router as query_route
from src.config import SystemConfig

logger.add("./logs/xgrapher.log", rotation="5 MB")
logger.info("Initializing application : xgrapher")

app = FastAPI(
    title="XGrapher",
    description="CRU(xD) into ONgDB without any worries",
    version="0.1.0"
)

# logger.info("Adding <router> namespace route")
app.include_router(data_route)
app.include_router(query_route)


@app.on_event("startup")
def startup():
    logger.info("Loading configuration from env")
    SystemConfig.load()


@app.on_event("shutdown")
def startup():
    logger.info("System shutdown initiated")


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")
