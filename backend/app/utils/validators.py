from decimal import Decimal
from datetime import date
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.contract import Contract
from ..models.boq_item import BOQItem
from ..models.settlement import Settlement
from .exceptions import ValidationError

class DataValidator:
    @staticmethod
    def validate_contract_dates(start_date: date, end_date: date) -> None:
        """验证合同日期"""
        if start_date >= end_date:
            raise ValidationError("合同开始日期必须早于结束日期")

    @staticmethod
    def validate_contract_status(
        db: Session,
        contract_id: int,
        expected_status: Optional[str] = None
    ) -> None:
        """验证合同状态"""
        contract = db.query(Contract).get(contract_id)
        if not contract:
            raise ValidationError("合同不存在")
        
        if expected_status and contract.status != expected_status:
            raise ValidationError(f"合同状态必须为 {expected_status}")

    @staticmethod
    def validate_boq_item_quantities(
        db: Session,
        boq_item_id: int,
        quantity: Decimal
    ) -> None:
        """验证工程量清单数量"""
        if quantity <= 0:
            raise ValidationError("数量必须大于0")

    @staticmethod
    def validate_settlement_date(
        db: Session,
        contract_id: int,
        settlement_date: date
    ) -> None:
        """验证结算日期"""
        contract = db.query(Contract).get(contract_id)
        if not contract:
            raise ValidationError("合同不存在")
        
        if settlement_date < contract.start_date:
            raise ValidationError("结算日期不能早于合同开始日期")
        
        if settlement_date > contract.end_date:
            raise ValidationError("结算日期不能晚于合同结束日期")

    @staticmethod
    def validate_payment_amount(
        db: Session,
        settlement_id: int,
        payment_amount: Decimal
    ) -> None:
        """验证付款金额"""
        if payment_amount <= 0:
            raise ValidationError("付款金额必须大于0")
        
        settlement = db.query(Settlement).get(settlement_id)
        if not settlement:
            raise ValidationError("结算记录不存在")
        
        # 检查付款总额是否超过结算金额
        total_paid = db.query(
            db.func.sum(Payment.payment_amount)
        ).filter(
            Payment.settlement_id == settlement_id
        ).scalar() or Decimal('0')
        
        if (total_paid + payment_amount) > settlement.settlement_amount:
            raise ValidationError("付款总额不能超过结算金额") 