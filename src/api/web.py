from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.schemas.parcels import ParcelFiltersDTO
from src.api.dependencies import DBDep, SessionIdDep

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def home_page(request: Request, session_id: SessionIdDep, db: DBDep):
    parcels = []
    if session_id:
        filters = ParcelFiltersDTO(limit=10, offset=0)
        parcels = await db.parcels.get_all(session_id, filters)
    types = await db.types.get_all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"session_id": session_id, "parcels": parcels, "types": types},
    )
