from paper_app import db

class Author(db.Model):
    __tablename__ = 'author'
    
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(128),nullable=False,unique=True)
    many_paper_authors = db.relationship('Paper_Author',back_populates='one_author',cascade='all, delete')

    def __repr__(self):
        return f"Author {self.name}"