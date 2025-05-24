from fastapi import APIRouter, Depends, Request, Form, Path, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.authentification.dependencies import permission_required
from src.core.cruds.dependencies import get_role_by_id
from src.core.cruds.roles import (
    create_role,
    update_role,
    delete_role,
    get_all_roles,
)
from src.core.models import db_helper, Role
from src.core.schemas.roles import RoleCreate, RoleUpdate

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")


@router.get(
    "/",
    response_model=list[Role],
    dependencies=[Depends(permission_required("read_all_roles"))],
)
async def read_roles(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return get_all_roles(session, skip, limit)


@router.post(
    "/",
    response_model=Role,
    status_code=201,
    dependencies=[Depends(permission_required("create_role"))],
)
async def create_new_role(
    role: RoleCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return create_role(session=session, role_in=role)


@router.get(
    "/{role_pk}",
    response_model=Role,
    dependencies=[Depends(permission_required("read_role"))],
)
async def read_role(
    role: Role = Depends(get_role_by_id),
):
    return role


@router.put(
    "/{role_pk}",
    response_model=Role,
    dependencies=[Depends(permission_required("update_role"))],
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
    dependencies=[Depends(permission_required("delete_role"))],
)
async def delete_role_endpoint(
    role: Role = Depends(get_role_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not delete_role(session=session, role=role):
        raise HTTPException(status_code=404, detail="Role not found")
