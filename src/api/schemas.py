from pydantic import BaseModel
from src.domain.enums import PackageStatus


class PackageStatusUpdateRequest(BaseModel):
    status: PackageStatus


class PackageResponse(BaseModel):
    id: str
    status: PackageStatus
    customer_address: str

    class Config:
        orm_mode = True