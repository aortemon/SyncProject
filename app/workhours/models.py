from sqlalchemy import Time
from sqlalchemy.orm import Mapped, mapped_column
from datetime import time
from database.model import Base, int_pk


class WorkHour(Base):
    id: Mapped[int_pk]
    starttime: Mapped[time] = mapped_column(Time, nullable=False)
    endtime: Mapped[time] = mapped_column(Time, nullable=False)
    lunchbreak_start: Mapped[time] = mapped_column(
        Time, nullable=False
    )
    lunchbreak_end: Mapped[time] = mapped_column(
        Time, nullable=False
    )
