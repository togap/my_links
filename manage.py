from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from settings import SQLALCHEMY_DATABASE_URI
from application.models import db
from run import app

migrate = Migrate(app, db)
manager = Manager(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
