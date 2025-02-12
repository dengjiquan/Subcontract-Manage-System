"""add triggers and indexes

Revision ID: 003
Revises: 002
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 添加索引
    op.create_index('ix_contracts_status', 'contracts', ['status'])
    op.create_index('ix_settlements_settlement_date', 'settlements', ['settlement_date'])
    op.create_index('ix_payments_payment_date', 'payments', ['payment_date'])
    
    # 添加复合索引
    op.create_index(
        'ix_settlement_details_settlement_boq',
        'settlement_details',
        ['settlement_id', 'boq_item_id'],
        unique=True
    )
    
    # 添加触发器：更新时间戳
    op.execute("""
        CREATE TRIGGER update_subcontractor_timestamp
        AFTER UPDATE ON subcontractors
        FOR EACH ROW
        BEGIN
            UPDATE subcontractors 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = OLD.id;
        END;
    """)
    
    op.execute("""
        CREATE TRIGGER update_contract_timestamp
        AFTER UPDATE ON contracts
        FOR EACH ROW
        BEGIN
            UPDATE contracts 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = OLD.id;
        END;
    """)
    
    op.execute("""
        CREATE TRIGGER update_boq_item_timestamp
        AFTER UPDATE ON boq_items
        FOR EACH ROW
        BEGIN
            UPDATE boq_items 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = OLD.id;
        END;
    """)
    
    op.execute("""
        CREATE TRIGGER update_settlement_timestamp
        AFTER UPDATE ON settlements
        FOR EACH ROW
        BEGIN
            UPDATE settlements 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = OLD.id;
        END;
    """)

def downgrade() -> None:
    # 删除触发器
    op.execute("DROP TRIGGER IF EXISTS update_subcontractor_timestamp")
    op.execute("DROP TRIGGER IF EXISTS update_contract_timestamp")
    op.execute("DROP TRIGGER IF EXISTS update_boq_item_timestamp")
    op.execute("DROP TRIGGER IF EXISTS update_settlement_timestamp")
    
    # 删除索引
    op.drop_index('ix_contracts_status')
    op.drop_index('ix_settlements_settlement_date')
    op.drop_index('ix_payments_payment_date')
    op.drop_index('ix_settlement_details_settlement_boq') 