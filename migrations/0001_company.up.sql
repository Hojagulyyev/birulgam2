CREATE TABLE IF NOT EXISTS company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(16) NOT NULL,
    
    CONSTRAINT company__uk__name UNIQUE (name)
);