from datetime import date
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field, EmailStr

if TYPE_CHECKING:
    from .contract import Contract

# 共享属性
class SubcontractorBase(BaseModel):
    name: str
    business_license: str
    contact_person: str
    contact_phone: str
    contact_email: EmailStr
    address: str
    tax_id: str
    bank_name: Optional[str] = None
    bank_account: Optional[str] = None
    status: str = Field(..., pattern='^(active|inactive|blacklisted)$')
    remarks: Optional[str] = None

# 创建时使用
class SubcontractorCreate(SubcontractorBase):
    pass

# 更新时使用
class SubcontractorUpdate(SubcontractorBase):
    name: Optional[str] = None
    business_license: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    status: Optional[str] = Field(None, pattern='^(active|inactive|blacklisted)$')

# 数据库模型转换
class SubcontractorInDBBase(SubcontractorBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

# API响应模型
class Subcontractor(SubcontractorInDBBase):
    pass

# 包含关系的响应模型
class SubcontractorWithContracts(SubcontractorInDBBase):
    contracts: List["Contract"] = []

    class Config:
        from_attributes = True 