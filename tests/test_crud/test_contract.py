import pytest
from datetime import date, timedelta
from fastapi import HTTPException
from app.crud.crud_contract import contract
from app.schemas.contract import ContractCreate, ContractUpdate

def test_create_contract(db_session):
    obj_in = ContractCreate(
        subcontractor_id=1,
        contract_number="TEST-001",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
        status="draft"
    )
    db_obj = contract.create(db=db_session, obj_in=obj_in)
    assert db_obj.contract_number == "TEST-001"
    assert db_obj.status == "draft"

def test_create_contract_invalid_dates(db_session):
    obj_in = ContractCreate(
        subcontractor_id=1,
        contract_number="TEST-002",
        start_date=date.today(),
        end_date=date.today() - timedelta(days=1),  # 结束日期早于开始日期
        status="draft"
    )
    with pytest.raises(HTTPException) as exc_info:
        contract.create(db=db_session, obj_in=obj_in)
    assert exc_info.value.status_code == 400
    assert "合同开始日期必须早于结束日期" in str(exc_info.value.detail) 