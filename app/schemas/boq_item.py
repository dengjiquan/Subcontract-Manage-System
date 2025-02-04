from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, constr

# 共享属性
class BOQItemBase(BaseModel):
    item_name: constr(min_length=1, max_length=200)
    unit_price: Decimal
    total_quantity: Decimal
    unit: constr(min_length=1, max_length=20)

# 创建时使用
class BOQItemCreate(BOQItemBase):
    contract_id: int

# 更新时使用
class BOQItemUpdate(BaseModel):
    item_name: Optional[constr(min_length=1, max_length=200)] = None
    unit_price: Optional[Decimal] = None
    total_quantity: Optional[Decimal] = None
    unit: Optional[constr(min_length=1, max_length=20)] = None

# 数据库模型转换
class BOQItemInDBBase(BOQItemBase):
    id: int
    contract_id: int
    total_price: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# API响应模型
class BOQItem(BOQItemInDBBase):
    pass 