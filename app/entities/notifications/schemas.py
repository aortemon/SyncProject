from pydantic import Field

from app.entities.common.schema import SchemaBase


class NotificationBase(SchemaBase):
    reciever_id: int = Field(..., description="ID of employee to notify")
    title: str = Field(..., description="Title of notication", max_length=256)
    description: str = Field(
        ..., description="Detailed notificatio info", max_length=256
    )
    link: str = Field(..., description="Link to redirect when onclick")


class SNewNotification(NotificationBase): ...
