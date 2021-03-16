CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR (200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  password VARCHAR(150) NOT NULL
);

CREATE TABLE tokens(
  id SERIAL PRIMARY KEY,
  value VARCHAR (64) NOT NULL,
  user_id INTEGER REFERENCES users NOT NULL
);
