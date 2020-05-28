# -*- coding:utf-8 -*-

import sys
import os
import secrets
from flask import Flask, render_template, redirect, session, url_for, request
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
        email = sign_in_form.data.get('email')
        session['email'] = email
        user = db.session.query(User).filter(User.email==email).first()
        user_id = user.id
        session['user_id'] = user_id
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
        db.session.add(user)
        db.session.commit()

        return redirect('/sign_in')

    return render_template('sign_up.html', sign_up_form=sign_up_form, user=user)

@app.route('/sign_out', methods=['GET'])
def sign_out():
    session.pop('email', None)
    session.pop('user_id', None)
    return redirect('/sign_in')

@app.route('/search', methods=['GET'])
def search():
    user = session.get('email', None)
    return render_template('search.html', user=user)

@app.route('/account', methods=['GET', 'POST'])
def account():
    user = session.get('email', None)
    if user is None:
        return redirect('/')
    else:
        user_id = session.get('user_id', None)
        user = db.session.query(User).filter(User.id == user_id).first()
        name = user.name
        description = user.description
        account_img = user.img_file
        account_img_url = url_for('static', filename='profile_img/' + account_img)
        return render_template('account.html', user=user, name=name, account_img_url=account_img_url, description=description)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_img', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@app.route('/account/change', methods=['GET', 'POST'])
def account_change():
    user = session.get('email', None)
    if user is None:
        return redirect('/')
    else:
        form = AccountEdit()
        user_id = session.get('user_id', None)
        user = db.session.query(User).filter(User.id == user_id).first()
        name = user.name
        description = user.description
        account_img = user.img_file
        account_img_url = url_for('static', filename='profile_img/' + account_img)
        if request.method == 'GET':
            return render_template('account_change.html', form=form, user=user, name=name, account_img_url=account_img_url, description=description)
        elif request.method == 'POST':
            if form.validate_on_submit():
                name = form.data.get('name')
                description = form.data.get('description')
                account_img = form.data.get('account_img')
                user.name = name
                user.description = description
                if account_img is not None:
                    picture_file = save_picture(account_img)
                    user.img_file = picture_file
                db.session.commit()
                return redirect('/account')
            else:
                return render_template('account_change.html', form=form, user=user, name=name, account_img_url=account_img_url, description=description)

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







