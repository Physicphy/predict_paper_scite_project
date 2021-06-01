from paper_app import db

class Predict_Result(db.Model):
    __tablename__ = 'predict_result'
    
    id = db.Column(db.Integer(),primary_key=True)
    result_name = db.Column(db.String(128),nullable=False)
    result_pickle = db.Column(db.PickleType(),nullable=False)
    published_date = db.Column(db.Date(),nullable=False)
    model_id = db.Column(db.Integer(),db.ForeignKey('predict_model.id',ondelete='CASCADE'), nullable=False)
    one_model = db.relationship('Predict_Model',back_populates='many_results')

    def __repr__(self):
        return f"Predict_Result {self.result_name}"