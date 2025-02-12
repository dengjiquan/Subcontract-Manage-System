from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal

# 付款共享属性
class PaymentBase(BaseModel):
    contract_id: int
    amount: Decimal
    payment_date: date
    payment_method: str = Field(..., pattern='^(cash|bank_transfer|check)$')
    description: Optional[str] = None
    reference_number: Optional[str] = None

# 付款创建
class PaymentCreate(PaymentBase):
    pass

# 付款更新
class PaymentUpdate(PaymentBase):
    contract_id: Optional[int] = None
    amount: Optional[Decimal] = None
    payment_date: Optional[date] = None
    payment_method: Optional[str] = Field(None, pattern='^(cash|bank_transfer|check)$')

# 付款数据库模型
class PaymentInDB(PaymentBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class Payment(PaymentInDB):
    pass

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
    upload_date: date

    class Config:
        from_attributes = True 