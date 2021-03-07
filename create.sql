CREATE TABLE books (
    book_id serial PRIMARY KEY
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
  review_id serial,
  r_user_id INTEGER REFERENCES users(id),
  r_book_id INTEGER REFERENCES books(book_id),
  review VARCHAR NOT NULL,
  PRIMARY KEY (review_id, r_user_id, r_book_id)
);

***column TYPE REFERENCES TABLE_NAME(COLUMN NAME),


CREATE TABLE gsa (
    ot VARCHAR NOT NULL,
    base VARCHAR NOT NULL,
    caso VARCHAR NOT NULL
  );
