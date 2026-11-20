from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    age= db.Column(db.Integer, nullable=True)
    education_level = db.Column(db.String(120), nullable=True)
    

    def __repr__(user):
        return f'<User {user.username}>'  
     
    def get_id(self):
        return str(self.id)