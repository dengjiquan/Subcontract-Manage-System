from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Settlement(Base):
    __tablename__ = "settlements"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    settlement_date = Column(Date, nullable=False)
    settlement_amount = Column(Numeric(15, 2), default=0)
    remarks = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    contract = relationship("Contract", back_populates="settlements")
    details = relationship("SettlementDetail", back_populates="settlement", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="settlement", cascade="all, delete-orphan")

class SettlementDetail(Base):
    __tablename__ = "settlement_details"

    id = Column(Integer, primary_key=True, index=True)
    settlement_id = Column(Integer, ForeignKey("settlements.id"), nullable=False)
    boq_item_id = Column(Integer, ForeignKey("boq_items.id"), nullable=False)
    completed_quantity = Column(Numeric(15, 2), nullable=False)
    settlement_amount = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    settlement = relationship("Settlement", back_populates="details")
    boq_item = relationship("BOQItem", back_populates="settlement_details") 