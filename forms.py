from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length


class SearchField(FlaskForm):
    title = StringField('Podaj nazwę filmu, który chcesz wyszukać:', validators=[DataRequired()])
    year = IntegerField('Podaj rok produkcji')
    submit = SubmitField('Wyszukaj')
    type = SelectField('Wybierz typ: ', choices=[('', ''),
                                                 ('movie', 'movie'),
                                                 ('series', 'series'),
                                                 ('episode', 'episode'),
                                                 ('game', 'game')])


class UserForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired('Field required')])
    last_name = StringField('Last name:', validators=[DataRequired('Field required')])
    age = StringField('Age:', validators=[DataRequired('Field required')])
    mail = StringField('Mail:', validators=[DataRequired('Field required')])
    phone = StringField('Phone number:', validators=[DataRequired('Field required')])
    submit = SubmitField('Add User')


class UserFormEdit(UserForm):
    submit = SubmitField('Confirm Edit User')