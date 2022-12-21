from userApp import db

class Batch(db.Model):
    __tablename__ = "batch"
    id = db.Column(db.Integer, primary_key=True)
    goods_number = db.Column(db.Integer)
    batch_date = db.Column(db.Date)
    id_provider = db.Column(db.Integer, db.ForeignKey("provider.id"), nullable=False)
    id_drug = db.Column(db.Integer, db.ForeignKey("drug.id"), nullable=False)
    supplay_contract = db.relationship('SupplayContract', backref='batch')
    @property
    def serialize(self):
        return {
            'id': self.id,
            'goods_number': self.goods_number,
            'batch_date': self.batch_date,
            'id_provider': self.id_provider,
            'id_drug': self.id_drug
        }