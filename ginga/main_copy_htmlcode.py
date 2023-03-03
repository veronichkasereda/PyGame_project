import os

from flask import Flask, url_for
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from db import __all_models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'My_secret_key'


class LoginForm(FlaskForm):
    userid = StringField('id Курицы', validators=[DataRequired()])
    userpass = PasswordField('password Курицы', validators=[DataRequired()])
    capid = StringField('id Главной курицы', validators=[DataRequired()])
    cappass = PasswordField('password Главной курицы', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/index/<stroka>')
def index(stroka):
    return render_template('base.html', title=stroka)


@app.route('/')
def main():
    return render_template('base.html', title='Mars')


@app.route('/galery', methods=['POST', 'GET'])
def galery():
    title = 'Пейзажи планеты Марс'
    pictures = os.listdir('static/img/galery')
    if request.method == 'GET':
        return render_template('galery.html',
                               pictures=pictures,
                               title=title,
                               lnp=len(pictures))
    elif request.method == 'POST':
        f = request.files['file']
        with open(f'static/img/galery/{len(pictures) + 1}.jpg', 'wb') as file:
            file.write(f.read())
        return redirect('/galery')
    return render_template('galery.html')


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    profil = {}
    profil['title'] = 'Анкета'
    profil['surname'] = 'Кукарека'
    profil['name'] = 'Куреку'
    profil['education'] = 'Высшее'
    profil['profession'] = 'Курица'
    profil['sex'] = 'Через годик понятно будет'
    profil['motivation'] = 'Достали земные дела'
    profil['ready'] = 'True'
    return render_template('auto_answer.html', profil=profil)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/succes')
    return render_template('login.html', title='Доступ', form=form)

@app.route('/succes')
def succes():
    #db_session.global_init("db/blogs.db")
    return  render_template('succes.html')


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof)


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1 align="center">Анкета претендента</h1>
                            <h3 align="center">на участие в миссии</h3>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="text" class="form-control" id="text" aria-describedby="emailHelp" placeholder="Фамилия" name="familia">
                                    <input type="text" class="form-control" id="text" placeholder="Имя" name="name">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="classSelect">В каком вы классе</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>высшее</option>
                                          <option>средне-специальное</option>
                                          <option>общее</option>
                                          <option>государь всея руси</option>
                                          <option>я лужа по жизни</option>
                                        </select>
                                     </div>
                                    <div class="form-group form-check">
                                    Ваша профессия<br>
                                       <input type="checkbox" class="form-check-input" id="profecy1" name="p1">
                                        <label class="form-check-label" for="acceptRules">инженер-исследователь</label>
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="profecy2" name="p2">
                                        <label class="form-check-label" for="acceptRules">пилот</label>
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="profecy3" name="p3">
                                        <label class="form-check-label" for="acceptRules">строитель</label>
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    <div class="form-group">
                                        <label for="about">Почему вы хотите участвовать в миссии</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готов остаться на Марсе</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['familia'])
        print(request.form['name'])
        print(request.form['class'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form['accept'])
        print(request.form['sex'])
        print(request.form['p1'])
        print(request.form['p2'])
        print(request.form['p3'])
        return "Форма отправлена"


if __name__ == '__main__':
    app.run()
