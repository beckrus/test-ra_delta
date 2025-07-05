import typing
from sqlalchemy import CheckConstraint, ForeignKey, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.models.parcels_types import ParcelTypesOrm

if typing.TYPE_CHECKING:
    from src.models.parcels_types import ParcelTypesOrm


class ParcelsOrm(Base):
    __tablename__ = "parcels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    weight: Mapped[float] = mapped_column(Float)
    cost_usd: Mapped[float] = mapped_column(Integer)
    delivery_cost: Mapped[float] = mapped_column(nullable=True)
    session_id: Mapped[str] = mapped_column(String(36), nullable=False)
    transport_company_id: Mapped[str] = mapped_column(Integer, nullable=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("types.id"), nullable=False)

    type: Mapped["ParcelTypesOrm"] = relationship("ParcelTypesOrm", back_populates="parcels")

    __table_args__ = (
        CheckConstraint("transport_company_id > 0", name="check_transport_company_id"),
    )
