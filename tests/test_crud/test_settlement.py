import pytest
from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from app.crud.crud_settlement import settlement
from app.schemas.settlement import (
    SettlementCreate,
    SettlementUpdate,
    SettlementDetailCreate
)
from .test_boq_item import test_create_boq_item

def test_create_settlement(db_session):
    # 创建测试数据
    boq_item_obj = test_create_boq_item(db_session)
    
    detail = SettlementDetailCreate(
        boq_item_id=boq_item_obj.id,
        completed_quantity=Decimal("5.00")  # 结算一半的数量
    )
    
    obj_in = SettlementCreate(
        contract_id=boq_item_obj.contract_id,
        settlement_date=date.today(),
        details=[detail]
    )
    
    db_obj = settlement.create_with_details(db=db_session, obj_in=obj_in)
    
    assert db_obj.settlement_amount == Decimal("500.00")  # 5 * 100
    assert len(db_obj.details) == 1
    assert db_obj.details[0].completed_quantity == Decimal("5.00")

def test_create_settlement_exceed_quantity(db_session):
    # 创建测试数据
    boq_item_obj = test_create_boq_item(db_session)
    
    detail = SettlementDetailCreate(
        boq_item_id=boq_item_obj.id,
        completed_quantity=Decimal("15.00")  # 超过合同数量
    )
    
    obj_in = SettlementCreate(
        contract_id=boq_item_obj.contract_id,
        settlement_date=date.today(),
        details=[detail]
    )
    
    with pytest.raises(HTTPException) as exc_info:
        settlement.create_with_details(db=db_session, obj_in=obj_in)
    assert exc_info.value.status_code == 400
    assert "结算数量超过合同数量" in str(exc_info.value.detail)

def test_update_settlement(db_session):
    # 创建测试数据
    boq_item_obj = test_create_boq_item(db_session)
    detail = SettlementDetailCreate(
        boq_item_id=boq_item_obj.id,
        completed_quantity=Decimal("5.00")
    )
    obj_in = SettlementCreate(
        contract_id=boq_item_obj.contract_id,
        settlement_date=date.today(),
        details=[detail]
    )
    db_obj = settlement.create_with_details(db=db_session, obj_in=obj_in)
    
    # 更新结算日期
    new_date = date.today().replace(day=1)
    obj_update = SettlementUpdate(settlement_date=new_date)
    updated_obj = settlement.update(
        db=db_session,
        db_obj=db_obj,
        obj_in=obj_update
    )
    
    assert updated_obj.settlement_date == new_date 