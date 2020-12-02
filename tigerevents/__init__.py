from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/EventsDB"
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] or "sqlite:///site.db"
app.config['SECRET_KEY'] = "7501d06b12422d9792968f951c600b32"
# The absolute path of the directory containing PDF files for users to download
app.config["USER_CAL"] = "/mnt/c/Users/Moin/Desktop/Tiger_Event/tigerevents/static/ical"

# Initialize the extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


from tigerevents.users.routes import users
from tigerevents.events.routes import events
from tigerevents.main.routes import main
from tigerevents.organizations.routes import organizations

app.register_blueprint(users)
app.register_blueprint(events)
app.register_blueprint(main)
app.register_blueprint(organizations)


