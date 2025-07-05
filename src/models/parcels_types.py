import typing
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


if typing.TYPE_CHECKING:
    from src.models.parcels import ParcelsOrm


class ParcelTypesOrm(Base):
    __tablename__ = "types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    parcels: Mapped[list["ParcelsOrm"]] = relationship("ParcelsOrm", back_populates="type")
