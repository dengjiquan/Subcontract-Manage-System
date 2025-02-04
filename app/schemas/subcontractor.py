from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, constr

# 共享属性
class SubcontractorBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    remarks: Optional[str] = None

# 创建时使用
class SubcontractorCreate(SubcontractorBase):
    pass

# 更新时使用
class SubcontractorUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    remarks: Optional[str] = None

# 数据库模型转换
class SubcontractorInDBBase(SubcontractorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# API响应模型
class Subcontractor(SubcontractorInDBBase):
    pass

# 包含关系的响应模型
class SubcontractorWithContracts(SubcontractorInDBBase):
    from .contract import Contract  # 避免循环导入
    contracts: List[Contract] = [] 