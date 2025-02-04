from decimal import Decimal
from sqlalchemy.orm import Session
from ..models.boq_item import BOQItem
from ..models.settlement import Settlement, SettlementDetail
from ..models.contract import Contract

class CalculationManager:
    @staticmethod
    def update_contract_amount(db: Session, contract_id: int) -> None:
        """更新合同总金额"""
        total_amount = db.query(
            db.func.sum(BOQItem.total_price)
        ).filter(
            BOQItem.contract_id == contract_id
        ).scalar() or Decimal('0')

        db.query(Contract).filter(
            Contract.id == contract_id
        ).update(
            {"contract_amount": total_amount},
            synchronize_session=False
        )

    @staticmethod
    def update_settlement_amount(db: Session, settlement_id: int) -> None:
        """更新结算金额"""
        total_amount = db.query(
            db.func.sum(SettlementDetail.settlement_amount)
        ).filter(
            SettlementDetail.settlement_id == settlement_id
        ).scalar() or Decimal('0')

        db.query(Settlement).filter(
            Settlement.id == settlement_id
        ).update(
            {"settlement_amount": total_amount},
            synchronize_session=False
        )

    @staticmethod
    def validate_settlement_quantity(
        db: Session,
        boq_item_id: int,
        completed_quantity: Decimal
    ) -> bool:
        """验证结算数量是否超过合同数量"""
        boq_item = db.query(BOQItem).get(boq_item_id)
        if not boq_item:
            return False

        total_settled = db.query(
            db.func.sum(SettlementDetail.completed_quantity)
        ).filter(
            SettlementDetail.boq_item_id == boq_item_id
        ).scalar() or Decimal('0')

        return (total_settled + completed_quantity) <= boq_item.total_quantity

    @staticmethod
    def calculate_settlement_amount(
        db: Session,
        boq_item_id: int,
        completed_quantity: Decimal
    ) -> Decimal:
        """计算结算金额"""
        boq_item = db.query(BOQItem).get(boq_item_id)
        if not boq_item:
            return Decimal('0')
        return completed_quantity * boq_item.unit_price 