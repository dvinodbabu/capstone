import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import json

app = Flask(__name__)
db = SQLAlchemy(app)

database_path = os.getenv('DATABASE_URL_HEROKU')

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def clean_start():
    db.drop_all()
    db.create_all()


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_json(self):
        return({
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone
        })

    def __repr__(self):
        return f'Actor: {self.id}, {self.name}'


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        print(123)
        db.session.delete(self)
        db.session.commit()

    def get_json(self):
        return({
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "release_date": self.release_date.isoformat()
        })

    def __repr__(self):
        return f'Movie:{self.id}, {self.title}'
