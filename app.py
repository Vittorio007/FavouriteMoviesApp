from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import logging
from datetime import date
from forms import SearchField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nasza_baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'fselifbes;fa;fopjfoi;nfnsfkn'
APIKEY = os.environ.get('APIKEY')
logging.basicConfig(level=logging.DEBUG,
                    filename=f'logs\\ {date.today()}.log',
                    format='%(asctime)s LEVEL: %(levelname)s MESSAGE: %(message)s')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

import models


@app.route('/')
@app.route('/home')
def home():
    app.logger.info('We are in home page !!!!')
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
    """

    """
    title = request.args.get('t')
    films = db.session.query(models.Film).filter_by(title=title.title()).all()
    filtered_films = []
    for film in films:
        filtered_films.append({'id': film.id, 'title': film.title, 'year': film.year})
    return jsonify(filtered_films)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """

    """
    form = SearchField()

    if request.method == 'POST':
        title = form.title.data
        year = form.year.data
        types = form.type.data
        params = {'s': title, 'y': year, 'type': types}
        params = {k: v for k, v in params.items() if v is not None}
        apikey = {'apikey': APIKEY}
        params.update(apikey)
        dane = requests.get('http://www.omdbapi.com/', params=params)
        filmfound = dane.json()
        try:
            films = [film for film in filmfound['Search'] if not
            db.session.query(models.Film).filter_by(film_id=film['imdbID']).all()]
            session['films'] = films
            app.logger.info(f'Tring found by: {params} - result: Found succes')
        except:
            flash('Nothing found.')
            app.logger.info(f'Tring found by: {params} - result: Nothing found')
            return redirect(url_for('search'))

        return render_template('result.html', films=films)

    return render_template('search.html', form=form)


@app.route('/details', methods=['GET', 'POST'])
def details():

    film_id = request.args.get('imdbID')
    params = {'i': film_id, 'apikey': APIKEY}
    dane = requests.get('http://www.omdbapi.com/', params=params)
    film = dane.json()
    item_name = film['Type'], film['Title']
    app.logger.info(f'Viewing details of {item_name}')

    return render_template('details.html', film=film)


@app.route('/filmlist', methods=['GET', 'POST'])
def film_list():
    films = session['films']
    return render_template('result.html', films=films)


@app.route('/filmadding', methods=['GET', 'POST'])
def film_adding():

    title_to_add = request.args.get('title')
    params = {'t': title_to_add,
              'apikey': APIKEY}
    dane = requests.get('http://www.omdbapi.com/', params=params)
    film_to_add = dane.json()
    film = models.Film(film_to_add['Title'],
                       film_to_add['Year'],
                       film_to_add['Runtime'],
                       film_to_add['Director'],
                       film_to_add['imdbID']
                       )
    db.session.add(film)
    db.session.commit()
    item_to_logs = (film_to_add['Type'], film_to_add['Title'])
    app.logger.info(f'Added {item_to_logs}to list')
    return redirect(url_for('films_list'))


@app.route('/filmdelete', methods=['GET'])
def film_delete():
    title = request.args.get('title')
    film_to_delete = db.session.query(models.Film).filter_by(title=title)
    app.logger.info(f'{title} was deleted from list.')
    film_to_delete.delete()
    db.session.commit()
    return redirect(url_for('films_list'))


if __name__ == '__main__':
    app.run(debug=True)
