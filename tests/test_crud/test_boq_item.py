import pytest
from decimal import Decimal
from fastapi import HTTPException
from app.crud.crud_boq_item import boq_item
from app.schemas.boq_item import BOQItemCreate, BOQItemUpdate
from .test_contract import test_create_contract  # 用于创建测试合同

def test_create_boq_item(db_session):
    # 先创建一个合同
    contract_obj = test_create_contract(db_session)
    
    obj_in = BOQItemCreate(
        contract_id=contract_obj.id,
        item_name="测试项目",
        unit_price=Decimal("100.00"),
        total_quantity=Decimal("10.00"),
        unit="m2"
    )
    db_obj = boq_item.create_with_contract(
        db=db_session, 
        obj_in=obj_in,
        contract_id=contract_obj.id
    )
    
    assert db_obj.item_name == "测试项目"
    assert db_obj.total_price == Decimal("1000.00")  # 100 * 10

def test_create_boq_item_invalid_price(db_session):
    contract_obj = test_create_contract(db_session)
    
    obj_in = BOQItemCreate(
        contract_id=contract_obj.id,
        item_name="测试项目",
        unit_price=Decimal("0.00"),  # 无效的单价
        total_quantity=Decimal("10.00"),
        unit="m2"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        boq_item.create_with_contract(
            db=db_session,
            obj_in=obj_in,
            contract_id=contract_obj.id
        )
    assert exc_info.value.status_code == 400
    assert "单价必须大于0" in str(exc_info.value.detail)

def test_update_boq_item(db_session):
    # 创建测试数据
    contract_obj = test_create_contract(db_session)
    obj_in = BOQItemCreate(
        contract_id=contract_obj.id,
        item_name="测试项目",
        unit_price=Decimal("100.00"),
        total_quantity=Decimal("10.00"),
        unit="m2"
    )
    db_obj = boq_item.create_with_contract(
        db=db_session,
        obj_in=obj_in,
        contract_id=contract_obj.id
    )
    
    # 更新数据
    obj_update = BOQItemUpdate(
        unit_price=Decimal("150.00")
    )
    updated_obj = boq_item.update(
        db=db_session,
        db_obj=db_obj,
        obj_in=obj_update
    )
    
    assert updated_obj.unit_price == Decimal("150.00")
    assert updated_obj.total_price == Decimal("1500.00")  # 150 * 10 