from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk


class Role(Base):
    id: Mapped[int_pk]
    description: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False
    )
