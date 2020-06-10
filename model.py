from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def add_user(self, name):
        u = User(name=name, password=password)
        db.session.add(u)
        db.session.commit()

class Book(db.Model):
    __tablename__="book_details"
