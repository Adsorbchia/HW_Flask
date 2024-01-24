from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(20), unique=True, nullable=False)
    user_password = db.Column(db.String())
    user_email = db.Column(db.String(30), unique=True, nullable=False)

  


    def set_password(self, user_password):
        self.user_password = generate_password_hash(user_password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)



    def __repr__(self):
        return f'User({self.user_login}, {self.user_email})'
