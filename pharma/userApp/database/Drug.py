from userApp import db

class Drug(db.Model):
    __tablename__ = "drug"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Float)
    id_provider = db.Column(db.Integer, db.ForeignKey("provider.id"), nullable=False)
    consist = db.Column(db.String(30))
    release_date = db.Column(db.Date)
    suitability = db.Column(db.Boolean)
    batch = db.relationship('Batch', backref='drug')
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'id_provider': self.id_provider,
            'consist': self.consist,
            'release_date': self.release_date,
            'suitability': self.suitability
        }