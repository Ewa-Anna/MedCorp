import os

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from .routes.routes import pages
from .routes.doctor import doctor
from .routes.auth import authorize
from .routes.admin import admin

from .db.models import User
from .db.db import db


migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    if config_name == 'test':
        app.config["SECRET_KEY"] = os.environ.get(
            "SECRET_KEY", "c544081efca90d112b80ff0ce139dd98")
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
        app.config["TESTING"] = True
    else:        
        app.config["SECRET_KEY"] = os.environ.get(
            "SECRET_KEY", "c544081efca90d112b80ff0ce139dd98")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prod.db'

    migrate.init_app(app, db)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(pages)
    app.register_blueprint(authorize)
    app.register_blueprint(doctor)
    app.register_blueprint(admin)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "authorize.login"


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app