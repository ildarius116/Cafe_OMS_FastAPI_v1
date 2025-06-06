from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.authentification.dependencies import permission_required
from src.core.cruds.dependencies import get_role_by_id
from src.core.cruds.roles import (
    create_role,
    update_role,
    delete_role,
    get_roles_list,
)
from src.core.models import db_helper, Role
from src.core.schemas.roles import RoleCreate, RoleUpdate, Role as RoleSchema

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")


@router.get(
    "/",
    response_model=list[RoleSchema],
    dependencies=[permission_required("read_all_roles")],
)
async def read_roles(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await get_roles_list(session=session)


@router.post(
    "/",
    response_model=RoleSchema,
    status_code=201,
    dependencies=[permission_required("create_role")],
)
async def create_new_role(
    role: RoleCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return create_role(session=session, role_in=role)


@router.get(
    "/{role_pk}",
    response_model=RoleSchema,
    dependencies=[permission_required("read_role")],
)
async def read_role(
    role: Role = Depends(get_role_by_id),
):
    return role


@router.put(
    "/{role_pk}",
    response_model=RoleSchema,
    dependencies=[permission_required("update_role")],
)
async def update_role_endpoint(
    role_update: RoleUpdate,
    role: Role = Depends(get_role_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    updated_role = update_role(session=session, role=role, role_update=role_update)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role


@router.delete(
    "/{role_pk}",
    status_code=204,
    dependencies=[permission_required("delete_role")],
)
async def delete_role_endpoint(
    role: Role = Depends(get_role_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not delete_role(session=session, role=role):
        raise HTTPException(status_code=404, detail="Role not found")
