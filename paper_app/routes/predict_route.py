from flask import Blueprint, request, redirect, url_for, Response
from paper_app.utils import main_func
from datetime import datetime


bp = Blueprint('prediction', __name__)

mfd = main_func.data_func()
mfm = main_func.model_func()

@bp.route('/model', methods=['POST'])
def make_model():
    request_data = request.form
    if not request_data:
        request_data = request.get_json()
    if request_data['keyword'] == '---' or request_data['keyword'] is None:
        all_paper = mfd.get_paper_from_db()
    else:
        all_paper = mfd.get_paper_filter_by_keyword(request_data['keyword'])
    
    if all_paper:
        p_dict_list =[]
        emb_dict_list =[]
        for p in all_paper:
            p_dict = {}
            # p_dict['id']=p.id
            p_dict['title']=p.title
            # p_dict['abstract']=p.abstract
            p_dict['category']=p.category_id
            p_dict['scites']=p.scites
            emb_dict = mfm.add_embedded_dict(p_dict,'title')
            p_dict.pop('title')
            p_dict_list.append(p_dict)
            emb_dict_list.append(emb_dict)
    
        train_df = mfm.make_df([p_dict_list,emb_dict_list])
        model = mfm.make_model(train_df,'scites')
        model_pickle = mfm.transform_to_pickle(model)
        mfm.add_model_to_db(request_data['model_name'],model_pickle)
    
    return redirect(url_for('main.model_index',msg_code=0))


@bp.route('/prediction', methods=['POST'])
@bp.route('/prediction/<result_name>')
def make_prediction(result_name=None):
    request_data = request.form
    if not request_data:
        request_data = request.get_json()

    if request_data['value'] == '' or request_data['value'] is None:
        if result_name is not None:
            return redirect(url_for('main.prediction_loaded_index',msg_code=1))

    model_row = mfm.get_model_from_db(request_data['model_name'])
    
    if model_row and model_row is not None:
        model = mfm.load_from_pickle(model_row.model_pickle)
    else:
        return redirect(url_for('main.prediction_index',msg_code=1))
    
    test_p_dict_list = mfm.get_test_data(request_data['key'],request_data['value'])

    raw_p_dict_list = []
    select_p_dict_list = []
    emb_dict_list = []
    if test_p_dict_list:
        for p_dict in test_p_dict_list:
            new_p_dict ={}
            check_category = mfd.check_and_add_category(p_dict['category'])
            new_p_dict['category'] = check_category.id
            p_dict['category'] = check_category.full_name
            emb_dict = mfm.add_embedded_dict(p_dict,'title')
            select_p_dict_list.append(new_p_dict)
            emb_dict_list.append(emb_dict)
            raw_p_dict_list.append(p_dict)
    
        test_df = mfm.make_df([select_p_dict_list,emb_dict_list])
        predict_result = mfm.make_prediction(model,test_df)
    
        raw_df = mfm.make_df([raw_p_dict_list])
        raw_df['scites'] = predict_result
        raw_df.sort_values(by='scites',axis=0,ascending=False,inplace=True)
        result_pickle = mfm.transform_to_pickle(raw_df)
    
        result_name_ = "[{}]_{}:{}_@{}".format(
            request_data['model_name'],
            request_data['key'],
            request_data['value'],
            datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            )
        mfm.add_prediction_to_db(result_name_,result_pickle,model_row.id)
        # result_dict_list = mfm.transform_predict_result_to_dict_list(raw_df,predict_result)
        return redirect(url_for('main.prediction_index',msg_code=0))
    else:
        return redirect(url_for('main.prediction_index',msg_code=1))

@bp.route('/model')
@bp.route('/model/<model_name>')
def delete_model(model_name=None):
    if model_name is None:
        return '',400
    elif mfm.get_model_from_db(model_name) is not None:
        mfm.delete_model(model_name)
        return redirect(url_for('main.model_index', msg_code=2))
    else:
        return '',404
