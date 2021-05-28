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

def delete_model(model_name):
    raw_model_list = Trained.query.filter_by(model_name=model_name).all()
    if raw_model_list:
        db.session.delete(raw_model_list[0])
        db.session.commit()
        return True
    else:
        return False