from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
# set the login_view to redirect users to login-page if they attempt to view
# restricted pages. redirects them to desired page once they're logged in
login.login_view = "login"

from app import routes, models
