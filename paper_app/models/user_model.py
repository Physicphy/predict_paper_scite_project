from paper_app import db

class Author(db.Model):
    __tablename__ = 'author'
    
    id = db.Column(db.BigInteger(),primary_key=True)
    username = db.Column(db.String(64),nullable=False)
    many_papers = db.relationship('Paper',back_populates='many_authors',cascade='all, delete-orphan')

    def __repr__(self):
        return f"Author {self.id}"


