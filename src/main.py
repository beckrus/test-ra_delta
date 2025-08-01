import logging
from pathlib import Path
import sys
from fastapi.concurrency import asynccontextmanager
from fastapi.staticfiles import StaticFiles
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from src.api.parcels import router as parcel_router
from src.api.parcels_types import router as parcel_types_router
from src.api.tasks import router as tasks_router
from src.api.web import router as web_router
from src.tasks.taskiq import broker


FORMAT = "%(asctime)s::%(levelname)s::%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%d/%m/%Y %I:%M:%S")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        logging.info("Starting Taskiq broker")
        await broker.startup()
    yield
    if not broker.is_worker_process:
        logging.info("Closing Taskiq broker")
        await broker.shutdown()


app = FastAPI(title="POST", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="./src/static"), name="static")

app.include_router(parcel_router)
app.include_router(parcel_types_router)
app.include_router(tasks_router)
app.include_router(web_router)


if __name__ == "__main__":
    uv_settings = {
        "app": "main:app",
        "reload": False,
        "host": "0.0.0.0",
        "port": 8000,
        "log_level": "info",
    }
    uvicorn.run(**uv_settings)
