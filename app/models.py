from app import db, login_manager
from flask_login import UserMixin
import bcrypt
from datetime import datetime

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
    username = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    chat = db.Column(db.String(1500), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)


    def __init__(self,username,title, chat):

        self.username = username
        self.title = title
        self.chat = chat

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    comment = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, post_id, username, comment):
        self.post_id = post_id
        self.username = username
        self.comment = comment
        self.date = datetime.utcnow().strftime('%d/%m/%Y %H:%M')
    
db.create_all()
