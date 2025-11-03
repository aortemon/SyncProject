from sqlalchemy import String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column
from app.database import Base, int_pk


class Status(Base):
    id: Mapped[int_pk]
    alias: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "statuses"
