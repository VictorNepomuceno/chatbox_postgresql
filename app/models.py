from app import db, login_manager
from flask_login import UserMixin
import bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,autoincrement=True, primary_key = True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.LargeBinary, nullable=False)


    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    chat = db.Column(db.String(500), nullable=False)

    def __init__(self,username,title, chat):

        self.username = username
        self.title = title
        self.chat = chat


db.create_all()
