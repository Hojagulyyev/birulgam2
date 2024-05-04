CREATE TABLE IF NOT EXISTS user_ (
    id SERIAL PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    password VARCHAR(128) NOT NULL,
    
    company_id BIGINT REFERENCES company(id) ON DELETE CASCADE
);
ALTER TABLE user_
    ADD CONSTRAINT user__uk__username UNIQUE (username);
