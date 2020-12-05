from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy_searchable import make_searchable
import os


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/EventsDB"
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = "7501d06b12422d9792968f951c600b32"

# Initialize the extensions
db = SQLAlchemy(app)
make_searchable(self.Base.metadata)
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


