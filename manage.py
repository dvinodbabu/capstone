from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models.models import db, Artist, Movie

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    Artist(name="Liam Neeson", age="40", gender="male", phone="11122233344").insert()
    Artist(name="Madonna", age="40", gender="female", phone="4433221122").insert()
    
    Movie(title="Titanic", genre="drama", release_date='2020/01/01').insert()
    Movie(title="Avatar", genre="fantasy", release_date='2021/01/01').insert()


if __name__ == '__main__':
    manager.run()