from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import (generate_password_hash,
        check_password_hash)

db = SQLAlchemy()

tags = db.Table('link_tags',
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
        db.Column('link_id', db.Integer, db.ForeignKey('link.id'))
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(10))
    email = db.Column(db.String(20), unique=True)
    bio = db.Column(db.Text)
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(30))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, username, password, email, bio, name, last_name):
        self.username = username
        self.password = password
        self.email = email
        self.bio = bio
        self.name = name
        self.last_name = last_name
        self.created = datetime.now()
        self.updated = None

    def __repr__(self):
        return self.username

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    state = db.Column(db.Boolean)
    favorite = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
            backref=db.backref('links', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=tags,
            backref=db.backref('links', lazy='dynamic'))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, url, user):
        self.url = url
        self.user = user
        self.state = False
        self.favorite = False
        self.created = datetime.now()
        self.updated = None

    def __repr__(self):
        return self.url

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
            backref=db.backref('tags', lazy='dynamic'))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, name, user):
        self.name = name
        self.user = user

    def __repr__(self):
        return self.name
