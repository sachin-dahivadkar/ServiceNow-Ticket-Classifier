from flask_login import UserMixin
from app import db
from app import login_manager


class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #email=db.Column(db.String(100))
    

    def __init__(self, username, password):
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))
