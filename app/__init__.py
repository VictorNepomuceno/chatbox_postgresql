from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost: 5433/chat'
app.secret_key = 'rootkey'


login_manager = LoginManager(app)
db = SQLAlchemy(app)
app.app_context().push()
