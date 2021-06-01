from paper_app import db

class Paper_Author(db.Model):
    __tablename__ = 'paper_author'
    id = db.Column(db.Integer(),primary_key=True)
    paper_id = db.Column(db.Integer(),db.ForeignKey('paper.id',ondelete="CASCADE"))
    author_id= db.Column(db.Integer(),db.ForeignKey('author.id',ondelete="CASCADE"))
    one_paper = db.relationship('Paper',back_populates='many_paper_authors')
    one_author = db.relationship('Author',back_populates='many_paper_authors')

class Paper_Keyword(db.Model):
    __tablename__ = 'paper_keyword'
    id = db.Column(db.Integer(),primary_key=True)
    paper_id = db.Column(db.Integer(),db.ForeignKey('paper.id',ondelete="CASCADE"))
    keyword_id= db.Column(db.Integer(),db.ForeignKey('keyword.id',ondelete="CASCADE"))
    one_paper = db.relationship('Paper',back_populates='many_paper_keywords')
    one_keyword = db.relationship('Keyword',back_populates='many_paper_keywords')

# class Paper_Category(db.Model):
#     __tablename__ = 'paper_category'
#     id = db.Column(db.Integer(),primary_key=True)
#     paper_id = db.Column(db.Integer(),db.ForeignKey('paper.id',ondelete="CASCADE"))
#     category_id= db.Column(db.Integer(),db.ForeignKey('category.id',ondelete="CASCADE"))
#     one_paper = db.relationship('Paper',back_populates='many_paper_categories')
#     one_category = db.relationship('Category',back_populates='many_paper_categories')


# paper_author = db.Table('paper_author',
#     db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True,ondelete="CASCADE"),
#     db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True,ondelete="CASCADE")
# )

# paper_keyword = db.Table('paper_keword',
#     db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True,ondelete="CASCADE"),
#     db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'), primary_key=True,ondelete="CASCADE")
# )

# paper_category = db.Table('paper_category',
#     db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True,ondelete="CASCADE"),
#     db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True,ondelete="CASCADE")
# )