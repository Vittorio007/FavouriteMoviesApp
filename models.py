from app import db


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.String)
    runtime = db.Column(db.String)
    director = db.Column(db.String)

    def __init__(self, title, year, runtime, director):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.director = director

