from io import BytesIO
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.auth.dependencies import ANY_USER, require_access
from app.employees.models import Employee
from app.files.dao import FilesDAO

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/get_by_id/")
async def get_task_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await FilesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found",
        )

    src = Path.home() / "SyncProject" / "user_files" / result.source[1:]
    print(src)
    with open(src, "rb") as file:
        buf = BytesIO(file.read())

    return StreamingResponse(
        buf,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(result.name)}"},
    )
