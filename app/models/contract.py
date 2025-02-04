from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    subcontractor_id = Column(Integer, ForeignKey("subcontractors.id"), nullable=False)
    contract_number = Column(String, unique=True, nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    contract_amount = Column(Numeric(15, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    subcontractor = relationship("Subcontractor", back_populates="contracts")
    boq_items = relationship("BOQItem", back_populates="contract", cascade="all, delete-orphan")
    settlements = relationship("Settlement", back_populates="contract", cascade="all, delete-orphan")
    files = relationship("ContractFile", back_populates="contract", cascade="all, delete-orphan") 