from datetime import date
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field
from decimal import Decimal

if TYPE_CHECKING:
    from .boq_item import BOQItem
    from .payment import Payment
    from .settlement import Settlement

class ContractBase(BaseModel):
    contract_number: str
    title: str
    description: Optional[str] = None
    subcontractor_id: int
    start_date: date
    end_date: date
    total_amount: Decimal
    status: str = Field(..., pattern='^(draft|active|completed|terminated)$')
    payment_terms: str
    retention_rate: Decimal = Field(ge=0, le=1)  # 保留金比例，0-1之间

class ContractCreate(ContractBase):
    pass

class ContractUpdate(ContractBase):
    contract_number: Optional[str] = None
    title: Optional[str] = None
    subcontractor_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = Field(None, pattern='^(draft|active|completed|terminated)$')
    payment_terms: Optional[str] = None
    retention_rate: Optional[Decimal] = Field(None, ge=0, le=1)

class ContractInDBBase(ContractBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class Contract(ContractInDBBase):
    pass

class ContractWithDetails(ContractInDBBase):
    boq_items: List["BOQItem"] = []
    payments: List["Payment"] = []
    settlements: List["Settlement"] = []

    class Config:
        from_attributes = True 