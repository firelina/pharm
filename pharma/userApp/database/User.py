from userApp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# класс
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(16))
    email = db.Column(db.String(255))
    hashed_password = db.Column(db.String(255))
    id_employee = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)


    @property
    def serialize(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'password': self.hashed_password,
            'data_id': self.data_id,
            'result_id': self.result_id
        }

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)