from userApp import db

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    id_drugstore = db.Column(db.Integer, db.ForeignKey("drugstore.id"), nullable=False)
    surname = db.Column(db.String(30))
    name = db.Column(db.String(20))
    fathername = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    telethon = db.Column(db.String(12))
    birthday = db.Column(db.Date)
    hire_date = db.Column(db.Date)
    salary = db.Column(db.Float)
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    supplay_contract = db.relationship('SupplayContract', backref='employee')
    user = db.relationship('User', backref='employee')
    @property
    def serialize(self):
        return {
            'id': self.id,
            'id_drugstore': self.id_drugstore,
            'surname': self.surname,
            'name': self.name,
            'fathername': self.fathername,
            'gender': self.gender,
            'telethon': self.telethon,
            'birthday': self.birthday,
            'hire_date': self.hire_date,
            'salary': self.salary
        }