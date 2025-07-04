from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from src.api.parcels import router as parcel_router
from src.api.parcels_types import router as parcel_types_router

app = FastAPI(title="POST")

app.include_router(parcel_router)
app.include_router(parcel_types_router)
