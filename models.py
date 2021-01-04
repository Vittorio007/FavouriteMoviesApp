from app import db


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.String)
    runtime = db.Column(db.String)
    director = db.Column(db.String)
    film_id = db.Column(db.String)

    def __init__(self, title, year, runtime, director, film_id):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.director = director
        self.film_id = film_id

