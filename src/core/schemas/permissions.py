from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int
