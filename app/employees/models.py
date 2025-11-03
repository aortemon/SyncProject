from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, str256, int_pk
from app.roles.models import Role
from app.schedules.models import Schedule

from datetime import datetime


class Employee(Base):
    id: Mapped[int_pk]
    lname: Mapped[str256]
    fname: Mapped[str256]
    mname: Mapped[str256]
    dob: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id"), nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False
    )
    phone: Mapped[str256]
    email: Mapped[str] = mapped_column(
        String(256),
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(256), default='1000', nullable=False
    )

    schedule: Mapped["Schedule"] = relationship("Schedule")
    role: Mapped["Role"] = relationship(lazy="selectin")

    extend_existing = True
