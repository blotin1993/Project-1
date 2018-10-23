CREATE TABLE books (
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);
CREATE TABLE users (
  id serial PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL,
  mail VARCHAR NOT NULL
);
CREATE TABLE reviews (
  user_id INTEGER REFERENCES users, FOREIGN KEY
  review TEXT
);



CREATE TABLE gsa (
    ot VARCHAR NOT NULL,
    base VARCHAR NOT NULL,
    caso VARCHAR NOT NULL
  );
