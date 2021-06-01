from paper_app.services import arxiv_api, embedding_api
from paper_app import db
from paper_app.models import paper_table, author_table, category_table, keyword_table, m_to_m_tables, predict_model_table, predict_result_table
from sklearn.ensemble import RandomForestRegressor as rfr
import pandas as pd
import pickle
from datetime import date, timedelta


def msg_processor(msg_code):
    '''
    msg_processor returns a msg object with 'msg', 'type'
    where 'msg' corresponds to the message user sees
    and 'type' is the color of the alert element

    codes:
        - 0 : Successfully added to database
        - 1 : It does not exist
        - 2 : Successfully deleted 
    '''

    msg_code = int(msg_code)

    msg_list = [
        (
            'Successfully added to database',
            'success'
        ),
        (
            'It does not exist',
            'warning'
        ),
        (
            'Successfully deleted',
            'info'
        )
    ]

    return {
        'msg':msg_list[msg_code][0],
        'type':msg_list[msg_code][1]
    }



class data_func:

    # def get_one_paper_from_arxiv(self,link_end,keyword):
    #     paper_dict = arxiv_api.get_paper(value=link_end,key='link_end',keyword=keyword)
    #     return paper_dict[0]


    def get_paper_from_db(self,link_end=None):
        if link_end is None:
            return paper_table.Paper.query.all()
        else:
            return paper_table.Paper.query.filter_by(link_end=link_end).one_or_none()

    def get_paper_filter_by_keyword(self,keyword):
        return paper_table.Paper.query \
                .join(paper_table.Paper.many_paper_keywords) \
                .join(m_to_m_tables.Paper_Keyword.one_keyword) \
                .filter(keyword_table.Keyword.word==keyword).all()

    def get_paper_filter_like(self,key,value):
        _value_ = "%{}%".format(value)
        if key == 'title':
            return paper_table.Paper.query.filter(paper_table.Paper.title.like(_value_)).all()
        elif key == 'abstract':
            return paper_table.Paper.query.filter(paper_table.Paper.abstract.like(_value_)).all()

    def get_keyword_from_db(self,keyword=None):
        if keyword is None:
            return keyword_table.Keyword.query.all()
        else:
            return keyword_table.Keyword.query.filter_by(word=keyword).one_or_none()

    def get_author_from_db(self,author=None):
        if author is None:
            return author_table.Author.query.all()
        else:
            return author_table.Author.query.filter_by(name=author).one_or_none()

    def get_category_from_db(self,category=None):
        if category is None:
            return category_table.Category.query.all()
        else:
            return category_table.Category.query.filter_by(short_name=category).one_or_none()
    
    def get_paper_keyword_from_db(self,paper_id,keyword_id):
        # paper_id = self.get_paper_from_db(link_end).id
        # keyword_id = self.get_keyword_from_db(keyword).id
        return m_to_m_tables.Paper_Keyword.query.filter_by(paper_id=paper_id,keyword_id=keyword_id).one_or_none()
    
    def get_paper_author_from_db(self,paper_id,author_id):
        # paper_id = self.get_paper_from_db(link_end).id
        # author_id = self.get_author_from_db(author).id
        return m_to_m_tables.Paper_Author.query.filter_by(paper_id=paper_id,author_id=author_id).one_or_none()


    def add_keyword(self,keyword):
        new_keyword = keyword_table.Keyword(word=keyword)
        db.session.add(new_keyword)
        db.session.commit()        

    def add_author(self,name):
        new_author = author_table.Author(name=name)
        db.session.add(new_author)
        db.session.commit()

    def add_category(self,short_category_name):
        main_cat = category_table.map_main[short_category_name.split('.')[0]]
        sub_cat = category_table.map_sub[short_category_name]
        full_category_name = main_cat+'\n: '+sub_cat
        new_category = category_table.Category(short_name=short_category_name,full_name=full_category_name)
        db.session.add(new_category)
        db.session.commit()

    def add_paper(self,link_end,title,abstract,published_date,scites,category_id):
        #title_embedded = embedding_api.get_embeddings([title])
        #abstract_embedded = embedding_api.get_embeddings([abstract])
        new_paper = paper_table.Paper(
            link_end=link_end,
            title=title,
            abstract=abstract,
            published_date=published_date,
            # title_embedded=title_embedded,
            # abstract_embedded=abstract_embedded,
            scites=scites,
            category_id=category_id)
        db.session.add(new_paper)
        db.session.commit()
        
    def add_paper_keyword(self,paper_id,keyword_id):
        new_paper_keyword = m_to_m_tables.Paper_Keyword(paper_id=paper_id,keyword_id=keyword_id)
        db.session.add(new_paper_keyword)
        db.session.commit()

    def add_paper_author(self,paper_id,author_id):
        new_paper_author = m_to_m_tables.Paper_Author(paper_id=paper_id,author_id=author_id)
        db.session.add(new_paper_author)
        db.session.commit()


    def update_paper(self,link_end,new_data_dict):
        _paper = self.get_paper_from_db(link_end)
        for key,value in new_data_dict.items():
            setattr(_paper,key,value)
        db.session.commit()

    def update_keyword(self,keyword,new_data_dict):
        _keyword = self.get_keyword_from_db(keyword)
        for key,value in new_data_dict.items():
            setattr(_keyword,key,value)
        db.session.commit()

    def update_author(self,author,new_data_dict):
        _author = self.get_author_from_db(author)
        for key,value in new_data_dict.items():
            setattr(_author,key,value)
        db.session.commit()

    def update_category(self,category,new_data_dict):
        _category = self.get_category_from_db(category)
        for key,value in new_data_dict.items():
            setattr(_category,key,value)
        db.session.commit()

    def update_paper_keyword(self,paper_id,keyword_id,new_data_dict):
        _pk = self.get_paper_keyword_from_db(paper_id,keyword_id)
        for key,value in new_data_dict.items():
            setattr(_pk,key,value)
        db.session.commit()

    def update_paper_author(self,paper_id,author_id,new_data_dict):
        _pa = self.get_paper_author_from_db(paper_id,author_id)
        for key,value in new_data_dict.items():
            setattr(_pa,key,value)
        db.session.commit()


    def delete_paper(self,link_end):
        _selection = self.get_paper_from_db(link_end)
        db.session.delete(_selection)
        db.session.commit()

    def delete_keyword(self,keyword):
        _selection = self.get_keyword_from_db(keyword)
        db.session.delete(_selection)
        db.session.commit()

    def delete_author(self,author):
        _selection = self.get_author_from_db(author)
        db.session.delete(_selection)
        db.session.commit()

    def delete_category(self,category):
        _selection = self.get_category_from_db(category)
        db.session.delete(_selection)
        db.session.commit()

    def delete_paper_keyword(self,paper_id,keyword_id):
        _selection = self.get_paper_keyword_from_db(paper_id,keyword_id)
        db.session.delete(_selection)
        db.session.commit()

    def delete_paper_author(self,paper_id,author_id):
        _selection = self.get_paper_author_from_db(paper_id,author_id)
        db.session.delete(_selection)
        db.session.commit()


    def get_paper_dict_list_from_arxiv(self,keyword,key,value,start_date=None,end_date=None):
        if start_date == '': start_date=None
        if end_date == '': end_date=None
        paper_dict_list = arxiv_api.get_paper(keyword=keyword,key=key,value=value,start_date=start_date,end_date=end_date)
        return paper_dict_list
    
    def check_and_add_category(self,short_name):
        check_category = self.get_category_from_db(short_name)
        if check_category is None:
            self.add_category(short_name)
            check_category = self.get_category_from_db(short_name)
        return check_category

    def add_paper_from_dict(self,paper_dict):
        link_end = paper_dict['link_end']
        title = paper_dict['title']
        abstract = paper_dict['abstract']
        published_date = paper_dict['published_date']
        scites = paper_dict['scites']
        category = self.check_and_add_category(paper_dict['category'])
        category_id = category.id
        self.add_paper(
            link_end=link_end,
            title=title,
            abstract=abstract,
            published_date=published_date,
            scites=scites,
            category_id=category_id
            )

    def check_and_add_author_list(self,author_list,paper_id):
        for author_name in author_list:
            check_author = self.get_author_from_db(author_name)
            if check_author is None:
                self.add_author(author_name)
                check_author = self.get_author_from_db(author_name)
            self.add_paper_author(paper_id=paper_id,author_id=check_author.id)

    def check_and_add_keyword(self,keyword,paper_id):
        check_keyword = self.get_keyword_from_db(keyword)
        if check_keyword is None:
            self.add_keyword(keyword)
            check_keyword = self.get_keyword_from_db(keyword)
            self.add_paper_keyword(keyword_id=check_keyword.id,paper_id=paper_id)
            return 'add keyword'
        check_paper_keyword = self.get_paper_keyword_from_db(keyword_id=check_keyword.id,paper_id=paper_id)
        if check_paper_keyword is None:
            self.add_paper_keyword(keyword_id=check_keyword.id,paper_id=paper_id)
            return 'add paper_keyword relation'

    def add_all_from_dict_list(self,paper_dict_list):
        for paper_dict in paper_dict_list:
            link_end = paper_dict['link_end']
            check_paper = self.get_paper_from_db(link_end)
            if check_paper is None:
                self.add_paper_from_dict(paper_dict)
                check_paper = self.get_paper_from_db(link_end)
                self.check_and_add_author_list(paper_dict['author_list'],check_paper.id)
            self.check_and_add_keyword(paper_dict['keyword'],check_paper.id)


class model_func:
    def get_test_data(self,key,value):
        start_date = (date.today() - timedelta(days=1)).strftime('%Y%m%d')
        end_date = (date.today()).strftime('%Y%m%d')
        paper_dict_list = arxiv_api.get_paper(keyword='',key=key.strip(),value=value.strip(),start_date=start_date,end_date=end_date)
        return paper_dict_list
    
    def add_embedded_dict(self,paper_dict,col_name):
        embedded_list = embedding_api.get_embeddings([paper_dict[col_name]])[0]
        emb_dict = {}
        for n, emb in enumerate(embedded_list):
            emb_dict[col_name+'_emb_'+str(n)] = emb
        return emb_dict

    def make_df(self,list_of_dict_list):
        df_list = []
        for dict_list in list_of_dict_list:
            _df = pd.DataFrame(dict_list)
            df_list.append(_df)
        tot_df = pd.concat(df_list,axis=1)
        return tot_df            

    def make_model(self,tot_df,target_col):
        model = rfr()
        target = tot_df[target_col]
        features = tot_df.drop(columns=target_col)
        model.fit(features,target)
        return model

    def make_prediction(self,model,features):
        predict_result = model.predict(features)
        return predict_result

    def transform_to_pickle(self,data):
        data_pickle = pickle.dumps(data)
        return data_pickle
    
    def load_from_pickle(self,data_pickle):
        data = pickle.loads(data_pickle)
        return data

    def add_model_to_db(self,model_name,model_pickle):
        new_model = predict_model_table.Predict_Model(model_name=model_name,model_pickle=model_pickle)
        db.session.add(new_model)
        db.session.commit()

    def add_prediction_to_db(self,result_name,result_pickle,model_id):
        new_result = predict_result_table.Predict_Result(
            result_name=result_name,
            result_pickle=result_pickle,
            published_date=date.today(),
            model_id=model_id)
        db.session.add(new_result)
        db.session.commit()
    
    def get_model_from_db(self,model_name=None):
        if model_name is None:
            return predict_model_table.Predict_Model.query.all()
        else:
            return predict_model_table.Predict_Model.query.filter_by(model_name=model_name).one_or_none()
    
    def get_result_from_db(self,result_name=None):
        if result_name is None:
            return predict_result_table.Predict_Result.query.order_by(predict_result_table.Predict_Result.id.desc()).all()
        else:
            return predict_result_table.Predict_Result.query.filter_by(result_name=result_name).one_or_none()

    def transform_predict_result_to_dict_list(self,result_df):
        result_dict_list = result_df.to_dict('records')
        return result_dict_list

    def delete_model(self,model_name):
        _selection = self.get_model_from_db(model_name)
        db.session.delete(_selection)
        db.session.commit()
