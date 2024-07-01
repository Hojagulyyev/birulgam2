CREATE TABLE IF NOT EXISTS deal (
    id SERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    store_id BIGINT NOT NULL REFERENCES store(id) ON DELETE CASCADE,
    created_by_id BIGINT NOT NULL REFERENCES user_(id) ON DELETE CASCADE,
    seller_id BIGINT DEFAULT NULL REFERENCES contact(id) ON DELETE CASCADE,
    buyer_id BIGINT DEFAULT NULL REFERENCES contact(id) ON DELETE CASCADE,

    store_code VARCHAR(2) NOT NULL,
    code_number INTEGER NOT NULL,    
    total_amount DECIMAL(10, 2) NOT NULL,
    remaining_amount_due DECIMAL(10, 2) NOT NULL,
    type VARCHAR(16) NOT NULL,

    installments_total_amount INTEGER NOT NULL DEFAULT 0,
    installments INTEGER NOT NULL DEFAULT 0,
    installment_amount INTEGER NOT NULL DEFAULT 0,
    installment_trifle INTEGER NOT NULL DEFAULT 0,
    installment_expiration_date DATE DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_paid_at TIMESTAMP DEFAULT NULL,
    closed_at TIMESTAMP DEFAULT NULL,
    note VARCHAR(255) DEFAULT NULL
);
