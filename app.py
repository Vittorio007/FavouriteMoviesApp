from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests

from forms import SearchField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nasza_baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'fselifbes;fa;fopjfoi;nfnsfkn'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


import models


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/filmslist')
def films_list():
    all = db.session.query(models.Film).all()
    return render_template('filmlist.html', all=all)


@app.route('/getfilm/<int:id>')
def get_film(id):
    film = db.session.query(models.Film).get(int(id))
    data = {'id': film.id, 'title': film.title, 'year': film.year}
    return jsonify(data)


@app.route('/getfilms')
def get_films():
    title = request.args.get('t')
    films = db.session.query(models.Film).filter_by(title=title.title()).all()
    filtered_films = []
    for film in films:
        filtered_films.append({'id': film.id, 'title': film.title, 'year': film.year})
    return jsonify(filtered_films)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchField()

    if request.method == 'POST':
        title = form.title.data
        year = form.year.data
        params = {'s': title, 'y': year}
        params = {k: v for k, v in params.items() if v is not None}
        apikey = {'apikey': '2324a7e9'}
        params.update(apikey)
        dane = requests.get('http://www.omdbapi.com/', params=params)
        filmfound = dane.json()
        print(filmfound)
        session['filmfound'] = filmfound

        return render_template('result.html', filmfound=filmfound)

    return render_template('search.html', form=form)


@app.route('/filmadding')
def film_adding():
    film = models.Film(session['filmfound']['Title'],
                       session['filmfound']['Year'],
                       session['filmfound']['Runtime'],
                       session['filmfound']['Director']
                       )
    db.session.add(film)
    db.session.commit()

    return redirect(url_for('films_list'))


@app.route('/filmdelete', methods=['GET'])
def film_delete():
    film_id = request.args.get('id')
    print(film_id)
    film_to_delete = db.session.query(models.Film).filter_by(id=film_id)
    film_to_delete.delete()
    db.session.commit()

    return redirect(url_for('films_list'))


if __name__ == '__main__':
    app.run(debug=True)
