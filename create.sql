CREATE TABLE book_user (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL
);

CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn VARCHAR NOT NULL,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);

CREATE TABLE reviews(
  id SERIAL PRIMARY KEY,
  book_id INTEGER REFERENCES books,
  user_id INTEGER REFERENCES book_user,
  user_review_score INTEGER NOT NULL,
  user_review VARCHAR NOT NULL
);
