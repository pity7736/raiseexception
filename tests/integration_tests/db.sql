CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(200) NOT NULL UNIQUE,
  password VARCHAR(150) NOT NULL
);
