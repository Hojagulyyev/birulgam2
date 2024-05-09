CREATE TABLE IF NOT EXISTS contact (
    id SERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    
    first_name VARCHAR(20) NOT NULL,
    surname VARCHAR(24) DEFAULT NULL,
    patronymic VARCHAR(24) DEFAULT NULL,
    phone VARCHAR(24) DEFAULT NULL,
    address VARCHAR(255) DEFAULT NULL,
    birthday timestamp DEFAULT NULL,
    gender VARCHAR(1) DEFAULT NULL,
    workplace VARCHAR(255) DEFAULT NULL,
    job_title VARCHAR(64) DEFAULT NULL,
    passport VARCHAR(11) DEFAULT NULL,
    passport_issued_date TIMESTAMP DEFAULT NULL,
    passport_issued_place VARCHAR(64) DEFAULT NULL,

    CONSTRAINT contact__uk__company_id__phone UNIQUE (company_id, phone)
);
