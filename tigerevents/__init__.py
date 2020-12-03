from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from tigerevents.config import Config
from sqlalchemy_searchable import make_searchable
import os

# Initialize the extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from tigerevents.users.routes import users
    from tigerevents.events.routes import events
    from tigerevents.main.routes import main
    from tigerevents.organizations.routes import organizations

    app.register_blueprint(users)
    app.register_blueprint(events)
    app.register_blueprint(main)
    app.register_blueprint(organizations)

    return app


