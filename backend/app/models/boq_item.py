from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class BOQItem(Base):
    __tablename__ = "boq_items"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    item_name = Column(String, nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    total_quantity = Column(Numeric(15, 2), nullable=False)
    unit = Column(String, nullable=False)
    total_price = Column(
        Numeric(15, 2),
        nullable=False,
        server_default=text("0"),
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    contract = relationship("Contract", back_populates="boq_items")
    settlement_details = relationship("SettlementDetail", back_populates="boq_item", cascade="all, delete-orphan") 