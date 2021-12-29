import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import json

app = Flask(__name__)
'''app.config.from_object('config')'''
db = SQLAlchemy(app)


DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost:5432') 
database_name = "casting"
database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, database_name)

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def clean_start():
    db.drop_all()
    db.create_all()

'''
def setup_data():
    Artist(name="Liam Neeson", age="40", gender="male", phone="11122233344").insert()
    Artist(name="Madonna", age="40", gender="female", phone="4433221122").insert()
    
    Movie(title="Titanic", genre="drama", release_date='2020/01/01').insert()
    Movie(title="Avatar", genre="fantasy", release_date='2021/01/01').insert()
''' 

class Artist(db.Model):
    __tablename__='Artist'
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

    def get_formatted_json(self):
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
    __tablename__='Movie'
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
        db.session.delete(self)
        db.session.commit()

    def get_formatted_json(self):
        return({
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "release_date": self.release_date.isoformat()
      
        })

    def __repr__(self):
        return f'Movie:{self.id}, {self.title}'