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
    password = db.Column(db.String(70))
    email = db.Column(db.String(20), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(30))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.set_password(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created = datetime.now()
        self.updated = None

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    url = db.Column(db.Text)
    description = db.Column(db.Text)
    author = db.Column(db.String(100))
    state = db.Column(db.Boolean)
    favorite = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
            backref=db.backref('links', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=tags,
            back_populates='links')
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, title, url, description, author, user):
        self.title = title
        self.url = url
        self.description = description
        self.author = author
        self.user = user
        self.state = False
        self.favorite = False
        self.created = datetime.now()
        self.updated = None

    def __repr__(self):
        return '<Link {}>'.format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
            backref=db.backref('tags', lazy='dynamic'))
    links = db.relationship('Link', secondary=tags,
            back_populates='tags')
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.created = datetime.now()
        self.updated = None

    def __repr__(self):
        return '<Tag {}>'.format(self.name)
