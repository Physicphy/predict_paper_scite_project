from paper_app import db

class Trained(db.Model):
    __tablename__ = 'trained'

    id = db.Column(db.BigInteger(),primary_key=True)
    model_name = db.Column(db.String())
    model_pkl = db.Column(db.PickleType())

    def __repr__(self):
        return f"Trained {self.id}"


def add_model(model_name,model_pkl):
    model_data = Trained(model_name=model_name,model_pkl=model_pkl)
    db.session.add(model_data)
    db.session.commit()