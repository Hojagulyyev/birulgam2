CREATE TABLE IF NOT EXISTS company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(16) NOT NULL
);

ALTER TABLE company
    ADD CONSTRAINT company__uk__name UNIQUE (name);