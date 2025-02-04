import pytest
from fastapi import HTTPException
from app.crud.crud_subcontractor import subcontractor
from app.schemas.subcontractor import SubcontractorCreate, SubcontractorUpdate

def test_create_subcontractor(db_session):
    obj_in = SubcontractorCreate(
        name="测试分包商",
        contact_name="张三",
        contact_phone="13800138000"
    )
    db_obj = subcontractor.create(db=db_session, obj_in=obj_in)
    assert db_obj.name == "测试分包商"
    assert db_obj.contact_name == "张三"

def test_create_duplicate_subcontractor(db_session):
    obj_in = SubcontractorCreate(
        name="测试分包商",
        contact_name="张三"
    )
    subcontractor.create(db=db_session, obj_in=obj_in)
    
    with pytest.raises(HTTPException) as exc_info:
        subcontractor.create(db=db_session, obj_in=obj_in)
    assert exc_info.value.status_code == 400
    assert "分包商名称已存在" in str(exc_info.value.detail)

def test_update_subcontractor(db_session):
    # 创建测试数据
    obj_in = SubcontractorCreate(
        name="测试分包商",
        contact_name="张三"
    )
    db_obj = subcontractor.create(db=db_session, obj_in=obj_in)
    
    # 更新数据
    obj_update = SubcontractorUpdate(contact_name="李四")
    updated_obj = subcontractor.update(
        db=db_session, db_obj=db_obj, obj_in=obj_update
    )
    assert updated_obj.contact_name == "李四"
    assert updated_obj.name == "测试分包商"  # 未更新的字段保持不变 