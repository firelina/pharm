from userApp import db

class SupplayContract(db.Model):
    __tablename__ = "supplyContract"
    id = db.Column(db.Integer, primary_key=True)
    id_batch = db.Column(db.Integer, db.ForeignKey("batch.id"), nullable=False)
    id_drugstore = db.Column(db.Integer, db.ForeignKey("drugstore.id"), nullable=False)
    contract_date = db.Column(db.Date)
    id_employee = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    notes = db.Column(db.String(30))
    @property
    def serialize(self):
        return {
            'id': self.id,
            'id_batch': self.id_batch,
            'id_drugstore': self.id_drugstore,
            'contract_date': self.contract_date,
            'id_employee': self.id_employee,
            'notes': self.notes
        }