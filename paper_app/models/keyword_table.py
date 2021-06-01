from paper_app import db

class Keyword(db.Model):
    __tablename__ = 'keyword'
    
    id = db.Column(db.Integer(),primary_key=True)
    word = db.Column(db.String(128),nullable=False,unique=True)
    many_paper_keywords = db.relationship('Paper_Keyword',back_populates='one_keyword',cascade='all, delete')

    def __repr__(self):
        return f"Keyword {self.word}"