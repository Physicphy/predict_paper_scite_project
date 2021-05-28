from paper_app import db

class Paper(db.Model):
    __tablename__ = 'paper'
    
    id = db.Column(db.BigInteger(),primary_key=True)
    title = db.Column(db.String(64),nullable=False)
    # many_authors = db.relationship('Author',back_populates='many_papers',cascade='all, delete-orphan')

    def __repr__(self):
        return f"Paper {self.id}"


