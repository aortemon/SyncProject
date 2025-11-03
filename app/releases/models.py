from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk, str256
from app.statuses.models import Status


class Release(Base):
    id: Mapped[int_pk]
    name: Mapped[str256]
    version: Mapped[str256]
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status_id: Mapped[int] = mapped_column(
        ForeignKey("statuses.id"), nullable=False
    )

    status: Mapped["Status"] = relationship("Status")
