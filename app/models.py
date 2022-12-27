from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import os

from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))


class Users(UserMixin, db.Model):
    __tableneame__='Users'
    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(300))

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
