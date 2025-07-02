import typing
from sqlalchemy import ForeignKey, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.models.parcels_types import ParcelTypesOrm

if typing.TYPE_CHECKING:
    from src.models.parcels_types import ParcelTypesOrm
    from src.models.sessions import SessionsOrm


class ParcelsOrm(Base):
    __tablename__ = "parcels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    weight: Mapped[float] = mapped_column(Float)
    cost_usd: Mapped[int] = mapped_column(Integer)

    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    session: Mapped["SessionsOrm"] = relationship("SessionsOrm", back_populates="parcels")

    type_id: Mapped[int] = mapped_column(ForeignKey("types.id"), nullable=False)

    type: Mapped["ParcelTypesOrm"] = relationship("ParcelTypesOrm", backref="parcels")
