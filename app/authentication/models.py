from flask_login import UserMixin
from datetime import datetime
from app import db

@login.user_loader
def load_user(user_id):
    return User.query.filter_by(userID=user_id).first()


class User(db.Model, UserMixin):

    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return self.userID