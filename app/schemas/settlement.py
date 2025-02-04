from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel

# 结算明细共享属性
class SettlementDetailBase(BaseModel):
    boq_item_id: int
    completed_quantity: Decimal

# 结算明细创建
class SettlementDetailCreate(SettlementDetailBase):
    pass

# 结算明细数据库模型
class SettlementDetailInDB(SettlementDetailBase):
    id: int
    settlement_id: int
    settlement_amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True

# 结算共享属性
class SettlementBase(BaseModel):
    settlement_date: date
    remarks: Optional[str] = None

# 结算创建
class SettlementCreate(SettlementBase):
    contract_id: int
    details: List[SettlementDetailCreate]

# 结算更新
class SettlementUpdate(BaseModel):
    settlement_date: Optional[date] = None
    remarks: Optional[str] = None

# 结算数据库模型
class SettlementInDBBase(SettlementBase):
    id: int
    contract_id: int
    settlement_amount: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 结算API响应模型
class Settlement(SettlementInDBBase):
    details: List[SettlementDetailInDB] = [] 