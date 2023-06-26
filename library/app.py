from flask import Flask
from routes import pages
from auth import authorize
import os
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager


db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "c544081efca90d112b80ff0ce139dd98")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    app.register_blueprint(pages)
    app.register_blueprint(authorize)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "authorize.login"
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    mail = Mail()
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = "example@example.com"
    app.config["MAIL_PASSWORD"] = "PASSWORD"
    mail.init_app(app)
    
    if __name__ == '__main__':
        app.run(debug=True)
    
    return app

