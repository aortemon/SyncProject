from sqlalchemy.orm import Mapped, relationship

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

    sun = relationship("WorkHour", foreign_keys="[Schedule.sun_id]", lazy="selectin")
    mon = relationship("WorkHour", foreign_keys="[Schedule.mon_id]", lazy="selectin")
    tue = relationship("WorkHour", foreign_keys="[Schedule.tue_id]", lazy="selectin")
    wed = relationship("WorkHour", foreign_keys="[Schedule.wed_id]", lazy="selectin")
    thu = relationship("WorkHour", foreign_keys="[Schedule.thu_id]", lazy="selectin")
    fri = relationship("WorkHour", foreign_keys="[Schedule.fri_id]", lazy="selectin")
    sat = relationship("WorkHour", foreign_keys="[Schedule.sat_id]", lazy="selectin")
