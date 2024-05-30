CREATE TABLE IF NOT EXISTS deal (
    id SERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    store_id BIGINT NOT NULL REFERENCES store(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES user_(id) ON DELETE CASCADE,
    seller_id BIGINT DEFAULT NULL REFERENCES contact(id) ON DELETE CASCADE,
    buyer_id BIGINT DEFAULT NULL REFERENCES contact(id) ON DELETE CASCADE,
    
    code VARCHAR(16) NOT NULL,
    total_amount INTEGER NOT NULL,
    remaining_amount_due INTEGER NOT NULL,
    type VARCHAR(16) NOT NULL,

    installments_total_amount INTEGER NOT NULL DEFAULT 0,
    installments INTEGER NOT NULL DEFAULT 0,
    installment_amount INTEGER NOT NULL DEFAULT 0,
    installment_trifle INTEGER NOT NULL DEFAULT 0,
    installment_expiration_date DATE DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_paid_at TIMESTAMP DEFAULT NULL,
    closed_at TIMESTAMP DEFAULT NULL,
    note VARCHAR(255) DEFAULT NULL,

    CONSTRAINT deal__uk__company_id__code UNIQUE (company_id, code)
);


CREATE FUNCTION increment_deal_code_by_store()
    RETURNS TRIGGER AS $$
DECLARE
    sale_id_seq INT;
    purchase_id_seq INT;
    deal_id_seq INT;
    store_code VARCHAR(2);
    deal_type_code VARCHAR(16);
BEGIN
    SELECT 
        next_sale_id,
        next_purchase_id,
        code
            INTO 
        sale_id_seq,
        purchase_id_seq,
        store_code
    FROM store 
        WHERE id = NEW.store_id;

    IF NEW.type = 'sale' THEN
        deal_id_seq := sale_id_seq;
        deal_type_code := LEFT(NEW.type, 2);

        UPDATE store 
            SET next_sale_id = sale_id_seq + 1 
        WHERE id = NEW.store_id;

    ELSIF NEW.type = 'purchase' THEN
        deal_id_seq := purchase_id_seq;
        deal_type_code := LEFT(NEW.type, 2);

        UPDATE store 
            SET next_purchase_id = purchase_id_seq + 1 
        WHERE id = NEW.store_id;
    END IF;
    
    NEW.code := CONCAT(
        UPPER(deal_type_code), '-', 
        UPPER(store_code), '-', 
        CAST(deal_id_seq AS TEXT)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER set_deal_code_before_insert
    BEFORE INSERT ON deal
FOR EACH ROW
    EXECUTE PROCEDURE increment_deal_code_by_store();