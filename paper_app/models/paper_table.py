from paper_app import db
# from paper_app.services import arxiv_api, embedding_api

class Paper(db.Model):
    __tablename__ = 'paper'
    
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(128),nullable=False)
    abstract = db.Column(db.Text(),nullable=False)
    link_end = db.Column(db.String(16),nullable=False,unique=True)
    published_date = db.Column(db.Date(),nullable=False)
    # title_embedded = db.Column(db.PickleType(),nullable=False)
    # abstract_embedded = db.Column(db.PickleType(),nullable=False)
    scites = db.Column(db.Integer(),nullable=False)
    category_id = db.Column(db.Integer(),db.ForeignKey('category.id',ondelete="CASCADE"),nullable=False)
    one_category = db.relationship('Category',back_populates='many_papers')
    many_paper_keywords = db.relationship('Paper_Keyword',back_populates='one_paper',cascade='all, delete')
    many_paper_authors = db.relationship('Paper_Author',back_populates='one_paper',cascade='all, delete')

    def __repr__(self):
        return f"Paper {self.title}"

# def add_paper(keyword,key,start_date,end_date):
#     paper_dict_list = arxiv_api.get_paper(keyword,key,start_date,end_date)
#     for paper_dict in paper_dict_list:
#         title_embedded = embedding_api.get_embeddings(paper_dict['title'].split())
#         abstract_embedded = embedding_api.get_embeddings(paper_dict['abstract'].split())
#         paper_data = Paper(
#             title=paper_dict['title'],
#             abstract=paper_dict['abstract'],
#             link_end=paper_dict['link_end'],
#             published_date=paper_dict['published_date'],
#             title_embedded=title_embedded,
#             abstract_embedded=abstract_embedded,
#             citation=paper_dict['citation'],
            
#             )
#         db.session.add(paper_data)
#     db.session.commit()

#     pass