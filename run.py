# -*- coding:utf-8 -*-

import sys
import os
from flask import Flask, render_template, redirect, session
from models import *
from forms import *
from api.v1 import api


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')

@app.route('/', methods=['GET', 'POST'])
def index():
    user = session.get('email', None)
    return render_template('index.html', user=user)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    user = session.get('email', None)
    sign_in_form = SignInForm()
    if sign_in_form.validate_on_submit():
        session['email'] = sign_in_form.data.get('email')
        return redirect('/')

    return render_template('sign_in.html', sign_in_form=sign_in_form, user=user)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    user = session.get('email', None)
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        user = User()
        user.name = sign_up_form.data.get('name')
        user.email = sign_up_form.data.get('email')
        user.password = sign_up_form.data.get('password')
        # print(sign_up_form.data.get('name'))
        # print(sign_up_form.data.get('email'))
        # print(sign_up_form.data.get('password'))
        db.session.add(user)
        db.session.commit()

        return redirect('/sign_in')

    return render_template('sign_up.html', sign_up_form=sign_up_form, user=user)

@app.route('/sign_out', methods=['GET'])
def sign_out():
    session.pop('email', None)
    return redirect('/sign_in')

@app.route('/search', methods=['GET'])
def search():
    user = session.get('email', None)
    return render_template('search.html', user=user)


basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'tirrilee.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tirrilee code test secret key'
db.init_app(app)
db.app = app
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000", debug=True)







