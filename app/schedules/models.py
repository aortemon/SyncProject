from sqlalchemy.orm import Mapped
from database.model import Base, int_pk, workhour_fk


class Schedule(Base):
    id: Mapped[int_pk]
    sun_id: Mapped[workhour_fk]
    mon_id: Mapped[workhour_fk]
    tue_id: Mapped[workhour_fk]
    wed_id: Mapped[workhour_fk]
    thu_id: Mapped[workhour_fk]
    fri_id: Mapped[workhour_fk]
    sat_id: Mapped[workhour_fk]