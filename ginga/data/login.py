from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    userid = StringField('id Курицы', validators=[DataRequired()])
    userpass = PasswordField('password Курицы', validators=[DataRequired()])
    capid = StringField('id Главной курицы', validators=[DataRequired()])
    cappass = PasswordField('password Главной курицы', validators=[DataRequired()])
    submit = SubmitField('Доступ')
