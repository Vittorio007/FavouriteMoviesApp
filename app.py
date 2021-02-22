from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from forms import SearchField, UserForm, UserFormEdit, UserLogIn
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'fselifbes;fa;fopjfoi;nfnsfkn'
APIKEY = os.environ.get('APIKEY')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import models

@login_manager.user_loader
def get_user(ident):
    return models.User.query.get(int(ident))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogIn()
    if request.method == 'POST':
        mail = form.mail.data
        password = form.password.data
        user_to_login = db.session.query(models.User).filter_by(mail=mail).first()
        if form.validate_on_submit():
            if check_password_hash(user_to_login.password, password):
                login_user(user_to_login)
                flash(f'Witaj {current_user.name} !')
                return redirect(url_for('home'))
            else:
                flash('Incorrect data for log in')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/filmslist')
@login_required
def films_list():
    """
    This take objects (models.Film) from data base and show in table.
    """
    all = db.session.query(models.Film).filter_by(user_id=current_user.id)
    return render_template('filmlist.html', all=all, login_user_id=current_user.id)


@app.route('/getfilm/<int:id>')
@login_required
def get_film(id):
    """
    This create JSON from object (models.Film) in data base.
    :param id: id of object (models.Film) in data base
    """
    film = db.session.query(models.Film).get(int(id))
    data = {'id': film.id, 'title': film.title, 'year': film.year}
    return jsonify(data)


@app.route('/getfilms')
@login_required
def get_films():
    """
    This create JSON from filtered objects (models.Film) in data base.
    """
    title = request.args.get('t')
    films = db.session.query(models.Film).filter_by(title=title.title()).all()
    filtered_films = []
    for film in films:
        filtered_films.append({'id': film.id, 'title': film.title, 'year': film.year})
    return jsonify(filtered_films)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    This searching data from API on site http://www.omdbapi.com/
    and show an screen results into table.
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
            db.session.query(models.Film).filter_by(user_id=session['user_id']).filter_by(film_id=film['imdbID']).all()]
            session['films'] = films
        except:
            flash('Nothing found.')
            return redirect(url_for('search'))

        return render_template('result.html', films=films)

    return render_template('search.html', form=form)


@app.route('/details', methods=['GET', 'POST'])
@login_required
def film_details():
    """
    This take details from API http://www.omdbapi.com/ by params and show results into table.
    """
    film_id = request.args.get('imdbID')
    params = {'i': film_id, 'apikey': APIKEY}
    dane = requests.get('http://www.omdbapi.com/', params=params)
    film = dane.json()
    item_name = film['Type'], film['Title']

    return render_template('filmDetails.html', film=film)


@app.route('/filmlist', methods=['GET', 'POST'])
@login_required
def film_list():
    """
    This show last searching into table taking from session memory.
    """
    films = session['films']
    return render_template('result.html', films=films)


@app.route('/filmadding', methods=['GET', 'POST'])
@login_required
def film_adding():
    """
    This add object (models.Film) to data base on log in user if it not yet on the list.
    """
    title_to_add = request.args.get('title')
    actual_user_films = db.session.query(models.Film).filter_by(user_id=current_user.id).\
        filter_by(title=title_to_add).first()
    if actual_user_films:
        flash('This film is on your list.')
    else:
        params = {'t': title_to_add,
                  'apikey': APIKEY}
        dane = requests.get('http://www.omdbapi.com/', params=params)
        film_to_add = dane.json()
        film = models.Film(current_user.id,
                           film_to_add['Title'],
                           film_to_add['Year'],
                           film_to_add['Runtime'],
                           film_to_add['Director'],
                           film_to_add['imdbID']
                           )
        db.session.add(film)
        db.session.commit()
    return redirect(url_for('films_list'))


@app.route('/filmdelete', methods=['GET'])
@login_required
def film_delete():
    """
    This delete object (models.Film) to data base.
    """
    title = request.args.get('title')
    film_to_delete = db.session.query(models.Film).filter_by(title=title)
    film_to_delete.delete()
    db.session.commit()
    return redirect(url_for('films_list'))


@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    """
    This add User into data base using form.
    """
    form = UserForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            user = models.User(form.name.data,
                               form.last_name.data,
                               form.age.data,
                               form.mail.data,
                               form.phone.data,
                               form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User was added correctly.')
            return redirect(url_for('user_list'))
    return render_template('adduser.html', form=form)


@app.route('/userdetails', methods=['GET'])
@login_required
def show_user_details():
    """
    This take object (models.User) and show into table details of this object (User).
    """
    user_details = db.session.query(models.User).filter_by(id=current_user.id).first()
    return render_template('userDetails.html',  user_details=user_details)


@app.route('/edituser', methods=['GET', 'POST'])
@login_required
def edit_user():
    """
    This edit User details by using form.
    """
    user_id = request.args.get('id')
    user_to_edit = db.session.query(models.User).filter_by(id=user_id)
    form = UserFormEdit()
    if request.method == 'POST':
        user_to_edit.update({'name': form.name.data,
                             'last_name': form.last_name.data,
                             'age': form.age.data,
                             'mail': form.mail.data,
                             'phone': form.phone.data})
        db.session.commit()
        flash("User was edit correct.")

        user_details = db.session.query(models.User).filter_by(id=user_id).first()
        return render_template('userDetails.html', user_details=user_details)

    return render_template('userEdit.html', form=form, user_to_edit=user_to_edit.first())


@app.route('/userdelete', methods=['GET'])
@login_required
def user_delete():
    """
    This delete object (models.User) to data base.
    """
    user_id = request.args.get('id')
    user_to_delete = db.session.query(models.User).filter_by(id=user_id)
    user_to_delete.delete()
    db.session.commit()
    return redirect(url_for('user_list'))


@app.route('/userslist')
@login_required
def user_list():
    """
    This take objects (models.Users) from data base and show into table.
    """
    all = db.session.query(models.User).all()
    return render_template('userList.html', all=all)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
