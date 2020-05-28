# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    img_file = db.Column(db.String(32), nullable=False, default='default.jpg')
    description = db.Column(db.String(32), nullable=True, default='소개글을 입력해주세요.')









