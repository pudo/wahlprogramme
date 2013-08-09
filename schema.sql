DROP TABLE IF EXISTS "votes";
CREATE TABLE "votes" (
  id SERIAL PRIMARY KEY,
  hash VARCHAR(100) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  source_ip VARCHAR(100) NOT NULL,
  party_guess VARCHAR(300),
  agree INTEGER,
  bullshit INTEGER
);
