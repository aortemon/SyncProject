from fastapi import APIRouter, Depends

from app.entities.admin.db_dumper import DatabaseUtils
from app.entities.auth.dependencies import UserRole, require_access
from app.entities.employees.models import Employee

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/db_dump/")
async def get_all_departments(
    compress: bool = True,
    include_data: bool = True,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    result = DatabaseUtils.do_backup(compress=compress, include_data=include_data)
    return {"message": f"OK. {result}"}
