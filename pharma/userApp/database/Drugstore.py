from userApp import db

class Drugstore(db.Model):
    __tablename__ = "drugstore"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    adress = db.Column(db.String(30))
    telethon = db.Column(db.String(12))
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    empolyee = db.relationship('Employee', backref='drugstore')
    supplay_contract = db.relationship('SupplayContract', backref='drugstore')
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'adress': self.adress,
            'telethon': self.telethon
        }