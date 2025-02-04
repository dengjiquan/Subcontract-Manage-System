from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, constr

# 共享属性
class ContractBase(BaseModel):
    contract_number: constr(min_length=1, max_length=50)
    start_date: date
    end_date: date
    status: constr(regex='^(draft|active|completed|terminated)$')

# 创建时使用
class ContractCreate(ContractBase):
    subcontractor_id: int

# 更新时使用
class ContractUpdate(BaseModel):
    contract_number: Optional[constr(min_length=1, max_length=50)] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[constr(regex='^(draft|active|completed|terminated)$')] = None

# 数据库模型转换
class ContractInDBBase(ContractBase):
    id: int
    subcontractor_id: int
    contract_amount: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# API响应模型
class Contract(ContractInDBBase):
    pass

# 包含关系的响应模型
class ContractWithDetails(ContractInDBBase):
    from .boq_item import BOQItem
    from .settlement import Settlement
    boq_items: List[BOQItem] = []
    settlements: List[Settlement] = [] 