CREATE TABLE IF NOT EXISTS users(
  id SERIAL PRIMARY KEY,
  username VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  password VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS tokens(
  id SERIAL PRIMARY KEY,
  value VARCHAR(64) NOT NULL,
  user_id INTEGER REFERENCES users NOT NULL
);

CREATE TABLE IF NOT EXISTS categories(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts(
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  title_slug VARCHAR(200) NOT NULL,
  body TEXT NOT NULL,
  state VARCHAR(30) NOT NULL,
  category_id INTEGER REFERENCES categories NOT NULL,
  author_id INTEGER REFERENCES users NOT NULL,
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  modified_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS post_comments(
  id SERIAL PRIMARY KEY,
  post_id INTEGER REFERENCES posts NOT NULL,
  state VARCHAR(30) NOT NULL,
  name VARCHAR(50),
  email VARCHAR(255),
  body TEXT NOT NULL,
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  modified_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
);
