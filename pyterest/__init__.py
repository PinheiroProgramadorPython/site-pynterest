from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dados_pynterest_user:5mldGzWsLudXQc2xmS6cpov9OeaHzcOJ@dpg-d1t1bcjuibrs738pdvag-a.oregon-postgres.render.com/dados_pynterest"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "cd4ca554a626be7a6e9aa6c057e3b140"
app.config["UPLOAD_FOLDER"] = "static/fotos-posts"

database = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "homepage"

bcrypt = Bcrypt(app)

from pyterest import routes
