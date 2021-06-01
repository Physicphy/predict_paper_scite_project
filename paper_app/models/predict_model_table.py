from paper_app import db

class Predict_Model(db.Model):
    __tablename__ = 'predict_model'
    
    id = db.Column(db.Integer(),primary_key=True)
    model_name = db.Column(db.String(128),nullable=False)
    model_pickle = db.Column(db.PickleType(),nullable=False)
    many_results = db.relationship('Predict_Result',back_populates='one_model',cascade='all, delete')

    def __repr__(self):
        return f"Predict_Model {self.model_name}"