from userApp import db

class Provider(db.Model):
    __tablename__ = "provider"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    adress = db.Column(db.String(30))
    telethon = db.Column(db.String(12))
    drug = db.relationship('Drug', backref='provider')
    batch = db.relationship('Batch', backref='provider')
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'adress': self.adress,
            'telethon': self.telethon
        }