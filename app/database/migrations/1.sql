CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS cookies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    domain TEXT,
    path TEXT,
    expiry INTEGER,
    httpOnly BOOLEAN,
    secure BOOLEAN,
    user_email TEXT,
    FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
);
