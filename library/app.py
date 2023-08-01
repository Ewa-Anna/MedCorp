import os
from config import Config
from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from .routes.routes import pages
from .routes.auth import authorize
from .routes.mail import mail

from .db.models import User
from .db.db import db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "c544081efca90d112b80ff0ce139dd98")

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config.from_object(Config)
migrate = Migrate(app, db)

db.init_app(app)
with app.app_context():
    db.create_all()

# app.config["MAIL_DEBUG"] = True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = EMAIL
app.config["MAIL_PASSWORD"] = PASSWORD
mail.init_app(app)

app.register_blueprint(pages)
app.register_blueprint(authorize)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "authorize.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
