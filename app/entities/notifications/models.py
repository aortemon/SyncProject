from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base, created_at, empls_fk, int_pk, str256

if TYPE_CHECKING:
    from app.entities.employees.models import Employee


# Предполагаю, что при нажатии на уведомление будет происходить редирект на
# сущность, породившую этот увед
class Notification(Base):
    id: Mapped[int_pk]
    reciever_id: Mapped[empls_fk]
    title: Mapped[str256]
    description: Mapped[str256]
    link: Mapped[str256]
    created_at: Mapped[created_at]
    is_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="FALSE", default=False
    )

    reciever: Mapped["Employee"] = relationship("Employee")
