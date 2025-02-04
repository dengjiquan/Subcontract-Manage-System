from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, constr, FilePath

# 付款共享属性
class PaymentBase(BaseModel):
    payment_date: date
    payment_amount: Decimal
    payment_method: constr(regex='^(cash|bank_transfer|check)$')
    remarks: Optional[str] = None

# 付款创建
class PaymentCreate(PaymentBase):
    settlement_id: int

# 付款更新
class PaymentUpdate(BaseModel):
    payment_date: Optional[date] = None
    payment_amount: Optional[Decimal] = None
    payment_method: Optional[constr(regex='^(cash|bank_transfer|check)$')] = None
    remarks: Optional[str] = None

# 付款数据库模型
class PaymentInDB(PaymentBase):
    id: int
    settlement_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 合同文件共享属性
class ContractFileBase(BaseModel):
    file_name: str
    file_path: str

# 合同文件创建
class ContractFileCreate(ContractFileBase):
    contract_id: int

# 合同文件数据库模型
class ContractFileInDB(ContractFileBase):
    id: int
    contract_id: int
    upload_date: datetime

    class Config:
        from_attributes = True 