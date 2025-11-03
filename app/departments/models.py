from sqlalchemy.orm import Mapped
from app.database import Base, int_pk, str256, empls_fk


class Department(Base):
    id: Mapped[int_pk]
    name: Mapped[str256]
    lead_id: Mapped[empls_fk]
