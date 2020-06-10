import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL="postgres://khwgtrmjmjgyqr:c7be07a0488d99e4cfa1d3524c2c9070b98a687632351c8739ee5186a31cb969@ec2-52-44-55-63.compute-1.amazonaws.com:5432/deudp50obrak6t"
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    print("i am inside main before opening csv")
    f = open("books.csv")
    print("i am inside main afte opening csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author,"year": year })
        print(f"Added book with 'isbn': {isbn}, 'title': {title}, 'author': {author},'year': {year}")
    db.commit()

if __name__ == "__main__":
    main()
