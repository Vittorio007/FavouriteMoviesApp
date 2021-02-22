from re import A

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields.html5 import EmailField, IntegerField


class SearchField(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    year = IntegerField('Year(optional)')
    submit = SubmitField('Search')
    type = SelectField('Type(optional): ', choices=[('', ''),
                                                    ('movie', 'movie'),
                                                    ('series', 'series'),
                                                    ('episode', 'episode'),
                                                    ('game', 'game')])


class UserLogIn(FlaskForm):
    mail = EmailField('Mail:', validators=[DataRequired('Field required')])
    password = StringField('Password:', validators=[DataRequired('Field required')])
    submit = SubmitField('Log In')


class UserForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired('Field required')])
    last_name = StringField('Last name:', validators=[DataRequired('Field required')])
    age = IntegerField('Age:', validators=[DataRequired('Field required')])
    mail = EmailField('Mail:', validators=[DataRequired('Field required')])
    phone = IntegerField('Phone number:', validators=[DataRequired('Field required')])
    password = PasswordField('Password:', validators=[DataRequired('Field required'),
                                                      Length(min=8, message='Password should has min 8 characters'),
                                                      Regexp('[A-Z]{1,}[a-z]{1,}[0-9]{1,}',
                                                             message='Password should has min one '
                                                                     'lower and uppercase letter and min one number')])
    submit = SubmitField('Add User')


class UserFormEdit(UserForm):
    submit = SubmitField('Confirm Edit User')
