from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String)
    year = db.Column(db.String)
    runtime = db.Column(db.String)
    director = db.Column(db.String)
    film_id = db.Column(db.String)

    def __init__(self, user_id, title, year, runtime, director, film_id):
        self.user_id = user_id
        self.title = title
        self.year = year
        self.runtime = runtime
        self.director = director
        self.film_id = film_id


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.String)
    mail = db.Column(db.String)
    phone = db.Column(db.Integer)
    password = db.Column(db.String)

    def __init__(self, name, last_name, age, mail, phone, password):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.mail = mail
        self.phone = phone
        self.password = generate_password_hash(password)


db.create_all()

