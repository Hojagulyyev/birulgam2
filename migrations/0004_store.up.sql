CREATE TABLE IF NOT EXISTS store (
    id SERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    
    name VARCHAR(26) NOT NULL,
    code VARCHAR(2) NOT NULL,
    next_deal_id INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT store__uk__company_id__name UNIQUE (company_id, name),
    CONSTRAINT store__uk__company_id__code UNIQUE (company_id, code)
);
