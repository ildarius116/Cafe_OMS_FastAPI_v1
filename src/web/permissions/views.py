from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.authentification.dependencies import permission_required
from src.core.cruds.dependencies import get_role_by_id, get_permission_by_id
from src.core.cruds.permissions import (
    update_permission,
    delete_permission,
    get_permissions_list,
    add_permission_to_role,
    remove_permission_from_role,
    create_permission,
)
from src.core.models import db_helper, Role, Permission
from src.core.schemas.permissions import (
    PermissionResponse,
    PermissionCreate,
    PermissionUpdate,
)
from src.core.schemas.roles import Role as RoleSchema

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")


@router.post(
    "/permissions/",
    response_model=PermissionResponse,
    status_code=201,
    dependencies=[Depends(permission_required("create_permission"))],
)
async def create_new_permission(
    permission: PermissionCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return create_permission(session=session, permission_in=permission)


@router.get(
    "/permissions/{permission_id}",
    response_model=PermissionResponse,
    dependencies=[Depends(permission_required("read_permission"))],
)
async def read_permission(
    permission: Permission = Depends(get_permission_by_id),
):
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.put(
    "/permissions/{perm_pk}",
    response_model=PermissionResponse,
    dependencies=[Depends(permission_required("update_permission"))],
)
async def update_permission_endpoint(
    permission_update: PermissionUpdate,
    permission: Permission = Depends(get_permission_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    updated_permission = update_permission(
        session=session,
        permission=permission,
        permission_update=permission_update,
    )
    if not updated_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return updated_permission


@router.delete(
    "/permissions/{perm_pk}",
    status_code=204,
    dependencies=[Depends(permission_required("delete_permission"))],
)
async def delete_permission_endpoint(
    permission: Permission = Depends(get_permission_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not delete_permission(session=session, permission=permission):
        raise HTTPException(status_code=404, detail="Permission not found")


@router.get(
    "/permissions/",
    response_model=list[PermissionResponse],
    dependencies=[Depends(permission_required("read_all_permissions"))],
)
async def read_permissions(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return get_permissions_list(session, skip, limit)


@router.post(
    "/roles/{role_pk}/permissions/{perm_pk}",
    response_model=RoleSchema,
    status_code=200,
    dependencies=[Depends(permission_required("add_permission_to_role"))],
)
async def add_permission_to_role_endpoint(
    role: Role = Depends(get_role_by_id),
    permission: Permission = Depends(get_permission_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    if permission in role.permissions:
        raise HTTPException(
            status_code=400, detail="Permission already assigned to role"
        )

    return add_permission_to_role(session=session, role=role, permission=permission)


@router.delete(
    "/roles/{role_pk}/permissions/{perm_pk}",
    response_model=RoleSchema,
    status_code=200,
    dependencies=[Depends(permission_required("remove_permission_from_role"))],
)
async def remove_permission_from_role_endpoint(
    role: Role = Depends(get_role_by_id),
    permission: Permission = Depends(get_permission_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return remove_permission_from_role(
        session=session, role=role, permission=permission
    )
