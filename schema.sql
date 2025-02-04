-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'user')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 分包商表
CREATE TABLE subcontractors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_name TEXT,
    contact_phone TEXT,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 合同表
CREATE TABLE contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subcontractor_id INTEGER NOT NULL,
    contract_number TEXT UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT CHECK(status IN ('draft', 'active', 'completed', 'terminated')) NOT NULL,
    contract_amount DECIMAL(15,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subcontractor_id) REFERENCES subcontractors(id)
);

-- 工程量清单项目表
CREATE TABLE boq_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    total_quantity DECIMAL(15,2) NOT NULL,
    unit TEXT NOT NULL,
    total_price DECIMAL(15,2) GENERATED ALWAYS AS (unit_price * total_quantity) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contracts(id)
);

-- 结算表
CREATE TABLE settlements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id INTEGER NOT NULL,
    settlement_date DATE NOT NULL,
    settlement_amount DECIMAL(15,2) DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contracts(id)
);

-- 结算明细表
CREATE TABLE settlement_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement_id INTEGER NOT NULL,
    boq_item_id INTEGER NOT NULL,
    completed_quantity DECIMAL(15,2) NOT NULL,
    settlement_amount DECIMAL(15,2) GENERATED ALWAYS AS (
        completed_quantity * (SELECT unit_price FROM boq_items WHERE id = boq_item_id)
    ) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (settlement_id) REFERENCES settlements(id),
    FOREIGN KEY (boq_item_id) REFERENCES boq_items(id)
);

-- 付款表
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    settlement_id INTEGER NOT NULL,
    payment_date DATE NOT NULL,
    payment_amount DECIMAL(15,2) NOT NULL,
    payment_method TEXT CHECK(payment_method IN ('cash', 'bank_transfer', 'check')) NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (settlement_id) REFERENCES settlements(id)
);

-- 合同文件表
CREATE TABLE contract_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contracts(id)
);

-- 创建触发器来更新合同金额
CREATE TRIGGER update_contract_amount
AFTER INSERT OR UPDATE OR DELETE ON boq_items
BEGIN
    UPDATE contracts 
    SET contract_amount = (
        SELECT COALESCE(SUM(total_price), 0)
        FROM boq_items
        WHERE contract_id = contracts.id
    )
    WHERE id = NEW.contract_id OR id = OLD.contract_id;
END;

-- 创建触发器来更新结算金额
CREATE TRIGGER update_settlement_amount
AFTER INSERT OR UPDATE OR DELETE ON settlement_details
BEGIN
    UPDATE settlements 
    SET settlement_amount = (
        SELECT COALESCE(SUM(settlement_amount), 0)
        FROM settlement_details
        WHERE settlement_id = settlements.id
    ),
    updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.settlement_id OR id = OLD.settlement_id;
END; 