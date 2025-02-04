export interface Subcontractor {
  id: number;
  name: string;
  contact_person: string;
  contact_phone: string;
  address: string;
  business_license: string;
  created_at: string;
  updated_at: string;
}

export interface Contract {
  id: number;
  subcontractor_id: number;
  contract_number: string;
  start_date: string;
  end_date: string;
  contract_amount: string;
  status: 'draft' | 'active' | 'completed' | 'terminated';
  remarks?: string;
  created_at: string;
  updated_at: string;
}

export interface BOQItem {
  id: number;
  contract_id: number;
  item_name: string;
  unit: string;
  unit_price: string;
  total_quantity: string;
  total_price: string;
  created_at: string;
  updated_at: string;
}

export interface Settlement {
  id: number;
  contract_id: number;
  settlement_date: string;
  settlement_amount: string;
  remarks?: string;
  details: SettlementDetail[];
  created_at: string;
  updated_at: string;
}

export interface SettlementDetail {
  id: number;
  settlement_id: number;
  boq_item_id: number;
  completed_quantity: string;
  settlement_amount: string;
}

export interface Stats {
  subcontractor_count: number;
  contract_count: number;
  total_contract_amount: string;
  total_settlement_amount: string;
} 