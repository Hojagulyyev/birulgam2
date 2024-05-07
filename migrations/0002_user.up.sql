CREATE TABLE IF NOT EXISTS user_ (
    id SERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES company(id) ON DELETE CASCADE,
    
    username VARCHAR(16) NOT NULL,
    password VARCHAR(128) NOT NULL
);

ALTER TABLE user_
    ADD CONSTRAINT user__uk__username UNIQUE (username);
