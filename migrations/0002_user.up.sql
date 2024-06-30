CREATE TABLE IF NOT EXISTS user_ (
    id SERIAL PRIMARY KEY,
    
    username VARCHAR(16) NOT NULL,
    password VARCHAR(128) NOT NULL,
    phone VARCHAR(11) NOT NULL,
    
    CONSTRAINT user__uk__username UNIQUE (username),
    CONSTRAINT user__uk__phone UNIQUE (phone)
);

CREATE TABLE IF NOT EXISTS user_company (
    user_id BIGINT NOT NULL REFERENCES user_(id) ON DELETE CASCADE,
    company_id BIGINT NOT NULL REFERENCES company(id) ON DELETE CASCADE,  
    PRIMARY KEY (user_id, company_id)
);
