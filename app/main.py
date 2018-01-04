from flask import Flask, render_template, request, url_for, redirect, session, flash
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import InputRequired, Email, Length
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.config.from_object(DevConfig)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    records = db.relationship('Record', backref='user', lazy='dynamic')

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self. email = email
        self.password = password

    def __repr__(self):
        return "<User '{}'>".format(self.username)

class Record(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), unique=True)
    volunteers = db.Column(db.String(255))
    notes = db.Column(db.Text())
    shopping_list = db.Column(db.Text())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __init__(self, date):
        self.date = date

    def __repr__(self):
        return "<Record '{}'>".format(self.title)

@app.route('/')
def index():
    return render_template('index.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Email(), validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(
            name = form.name.data,
            username = form.username.data,
            email = form.email.data,
            password = sha256_crypt.encrypt(str(form.password.data))
        )

        db.session.add(new_user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()