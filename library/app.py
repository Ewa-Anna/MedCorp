import os
from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from .routes.routes import pages
from .routes.doctor import doctor
from .routes.auth import authorize
from .routes.admin import admin
from .routes.mail import mail

from .db.models import User
from .db.db import db


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "c544081efca90d112b80ff0ce139dd98")

    load_dotenv()
    EMAIL_TO = os.environ.get("EMAIL_TO")
    EMAIL_FROM = os.environ.get("EMAIL_FROM")
    SMTP = os.environ.get("SMTP")
    PASSWORD = os.environ.get("PASSWORD")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    migrate.init_app(app, db)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.config["MAIL_SERVER"] = SMTP
    # app.config["MAIL_PORT"] = 587
    # app.config['MAIL_USE_TLS'] = True
    app.config["MAIL_PORT"] = 465
    app.config['MAIL_USE_SSL'] = True
    # app.config["MAIL_SUPPRESS_SEND"] = True  <-- uncomment this line in case you do not want to send emails
    app.config["MAIL_USERNAME"] = EMAIL_FROM
    app.config["MAIL_PASSWORD"] = PASSWORD
    mail.init_app(app)

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