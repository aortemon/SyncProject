from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.employees.models import Employee
from app.entities.meetings.dao import MeetingsDAO
from app.entities.meetings.schemas import SNewMeeting, SUpdateMeeting

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.get("/all/")
async def get_all_meetings(user_data: Employee = Depends(require_access(ANY_USER))):
    return await MeetingsDAO.find_all()


@router.get("/get_by_id/")
async def get_meeting_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await MeetingsDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found",
        )
    return result


@router.post("/add/")
async def add_meeting(
    response: Response,
    new_meeting: SNewMeeting,
    user_data: Employee = Depends(require_access(ANY_USER)),
):
    print(response)
    await MeetingsDAO.add(**new_meeting.dict())
    return {"message": "New department was added successfully!"}


@router.put("/update/")
async def update_meeting(
    response: Response,
    update: SUpdateMeeting,
    user_data: Employee = Depends(require_access(ANY_USER)),
):
    result = await MeetingsDAO.update(filter_by={"id": update.id}, **update.dict())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department was not updated. ID={update.id} not found",
        )
    return {"message": f"Department(id={update.id}) was updated successfully"}
