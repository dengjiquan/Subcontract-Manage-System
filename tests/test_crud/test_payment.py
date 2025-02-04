import pytest
from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from app.crud.crud_payment import payment
from app.schemas.payment import PaymentCreate, PaymentUpdate
from .test_settlement import test_create_settlement

def test_create_payment(db_session):
    # 创建测试数据
    settlement_obj = test_create_settlement(db_session)
    
    obj_in = PaymentCreate(
        settlement_id=settlement_obj.id,
        payment_date=date.today(),
        payment_amount=Decimal("300.00"),  # 支付部分金额
        payment_method="bank_transfer",
        remarks="首期付款"
    )
    
    db_obj = payment.create(db=db_session, obj_in=obj_in)
    
    assert db_obj.payment_amount == Decimal("300.00")
    assert db_obj.payment_method == "bank_transfer"

def test_create_payment_exceed_amount(db_session):
    # 创建测试数据
    settlement_obj = test_create_settlement(db_session)
    
    obj_in = PaymentCreate(
        settlement_id=settlement_obj.id,
        payment_date=date.today(),
        payment_amount=Decimal("600.00"),  # 超过结算金额
        payment_method="bank_transfer"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        payment.create(db=db_session, obj_in=obj_in)
    assert exc_info.value.status_code == 400
    assert "付款总额不能超过结算金额" in str(exc_info.value.detail)

def test_update_payment(db_session):
    # 创建测试数据
    settlement_obj = test_create_settlement(db_session)
    obj_in = PaymentCreate(
        settlement_id=settlement_obj.id,
        payment_date=date.today(),
        payment_amount=Decimal("300.00"),
        payment_method="bank_transfer"
    )
    db_obj = payment.create(db=db_session, obj_in=obj_in)
    
    # 更新付款方式
    obj_update = PaymentUpdate(
        payment_method="cash",
        remarks="改为现金支付"
    )
    updated_obj = payment.update(
        db=db_session,
        db_obj=db_obj,
        obj_in=obj_update
    )
    
    assert updated_obj.payment_method == "cash"
    assert updated_obj.remarks == "改为现金支付"

def test_multiple_payments(db_session):
    # 创建测试数据
    settlement_obj = test_create_settlement(db_session)
    
    # 第一次付款
    payment1 = PaymentCreate(
        settlement_id=settlement_obj.id,
        payment_date=date.today(),
        payment_amount=Decimal("200.00"),
        payment_method="bank_transfer",
        remarks="首期付款"
    )
    payment.create(db=db_session, obj_in=payment1)
    
    # 第二次付款
    payment2 = PaymentCreate(
        settlement_id=settlement_obj.id,
        payment_date=date.today(),
        payment_amount=Decimal("200.00"),
        payment_method="bank_transfer",
        remarks="二期付款"
    )
    payment.create(db=db_session, obj_in=payment2)
    
    # 第三次付款（应该失败，因为超过结算金额）
    payment3 = PaymentCreate(
        settlement_id=settlement_obj.id,
        payment_date=date.today(),
        payment_amount=Decimal("200.00"),
        payment_method="bank_transfer",
        remarks="三期付款"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        payment.create(db=db_session, obj_in=payment3)
    assert exc_info.value.status_code == 400
    assert "付款总额不能超过结算金额" in str(exc_info.value.detail) 