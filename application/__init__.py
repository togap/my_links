from flask import Flask

def create_app(config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config)
    from application.models import db
    db.init_app(app)
    return app
