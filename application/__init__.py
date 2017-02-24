from flask import Flask
from flask.ext.login import LoginManager

def create_app(config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config)
    from application.models import db
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    db.init_app(app)
    return app
