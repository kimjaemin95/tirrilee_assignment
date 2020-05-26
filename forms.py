# -*- coding:utf-8 -*-

from models import *
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, EqualTo


class SignUpForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    re_password = StringField('re_password', validators=[DataRequired(), EqualTo('password')])


class SignInForm(FlaskForm):
    class UserEmail(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            email = form['email'].data
            print(field.data)

            user = User.query.filter_by(email=email).first()
            if user is None:
                raise ValueError('Wrong Email!')

    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            email = form['email'].data
            password = field.data

            user = User.query.filter_by(email=email).first()
            if user is None:
                raise ValueError('Wrong Email!')
            elif user.password != password:
                raise ValueError('Wrong password!')


    email = StringField('email', validators=[DataRequired(), UserEmail()])
    password = StringField('password', validators=[DataRequired(), UserPassword()])
















