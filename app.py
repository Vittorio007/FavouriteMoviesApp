from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nasza_baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


@app.route('/')
@app.route('/home')
def home():
    pass
# year = 'y=2000'
#
# dane = requests.get(f'http://www.omdbapi.com/?apikey=2324a7e9&{year}')
#
# if dane.status_code == 200:
#     slownik = dane.json()
#     print(slownik)
#
# else:
#     print('coś poszło nie tak')
#

