from flask import Blueprint, render_template, request
from paper_app.utils import main_func
from paper_app.models import predict_model_table

bp = Blueprint('main', __name__)

mfd = main_func.data_func()
mfm = main_func.model_func()

# 시작 페이지
@bp.route('/')
def index():
    return render_template('index.html')

# 모델 관리 페이지
@bp.route('/model/')
def model_index():
    # DB에서 현재 학습모델들 리스트를 불러와 출력
    raw_model_list = mfm.get_model_from_db()
    model_list = [{"id":model.id,"model_name":model.model_name} for model in raw_model_list]
    
    # DB에서 현재 키워드 리스트를 불러와 출력
    raw_keyword_list = mfd.get_keyword_from_db()
    #keyword_list = [{'id':-1,'word':'---'}]+[{'id':keyword.id,'word':keyword.word} for keyword in raw_keyword_list]
    keyword_list = ['---']+[keyword.word for keyword in raw_keyword_list]

    # predict_route에서 온 msg_code 확인
    msg_code = request.args.get('msg_code', None)
    alert_msg = main_func.msg_processor(msg_code) if msg_code is not None else None

    return render_template('model.html', alert_msg=alert_msg, model_list=model_list, keyword_list=keyword_list)


# 논문 관리 페이지
@bp.route('/paper')
def paper_index():
    # DB에서 현재 논문들 리스트를 불러와 출력
    raw_paper_list = mfd.get_paper_from_db()
    paper_list =[] 
    if raw_paper_list:
        for p in raw_paper_list:
            author_list = [p_a.one_author.name for p_a in p.many_paper_authors]
            keyword_list = [p_w.one_keyword.word for p_w in p.many_paper_keywords]
            paper_list.append({
                "id":p.id,
                "title":p.title,
                "category":p.one_category.full_name,
                "author":author_list,
                "keyword":keyword_list,
                "scites":p.scites,
                "link_end":p.link_end,
                "published_date":p.published_date,
                "abstract":p.abstract
                })
    
    key_list = [
        {'k':'Identifier','v':'link_end'},
        {'k':'Abstract','v':'abstract'},
        {'k':'Title','v':'title'},
    ]

    # paper_route에서 온 msg_code 확인
    msg_code = request.args.get('msg_code', None)
    alert_msg = main_func.msg_processor(msg_code) if msg_code is not None else None

    return render_template('paper.html', alert_msg=alert_msg, paper_list=paper_list,key_list=key_list)


# 예측 결과 조회/관리 페이지
@bp.route('/prediction')
def prediction_index():
    msg_code = request.args.get('msg_code', None)
    alert_msg = main_func.msg_processor(msg_code) if msg_code is not None else None
    
    result_row = mfm.get_result_from_db()
    result_list = []
    prediction_dict_list = []

    if result_row and result_row is not None:
        result_list = [{"id":result.id,"result_name":result.result_name} for result in result_row]
        result_df = mfm.load_from_pickle(result_row[0].result_pickle)
        prediction_dict_list = mfm.transform_predict_result_to_dict_list(result_df)
    
    model_row = mfm.get_model_from_db()
    model_list = []

    if model_row and model_row is not None:
        model_list = [{"id":model.id,"model_name":model.model_name} for model in model_row]

    key_list = [
        {'k':'Identifier','v':'link_end'},
        {'k':'Abstract','v':'abstract'},
        {'k':'Title','v':'title'},
    ]

    return render_template(
        'prediction.html',alert_msg=alert_msg,
        prediction_list=prediction_dict_list,
        key_list=key_list,
        model_list=model_list,
        result_list=result_list
        )


# 예측 결과 조회 페이지
@bp.route('/prediction_loaded')
@bp.route('/prediction_loaded/<result_name>')
def prediction_loaded_index(result_name=None):
    msg_code = request.args.get('msg_code', None)
    alert_msg = main_func.msg_processor(msg_code) if msg_code is not None else None
    
    result_row = mfm.get_result_from_db()
    result_list = []
    prediction_dict_list = []

    if result_row and result_row is not None:
        result_list = [{"id":result.id,"result_name":result.result_name} for result in result_row]
        if result_name is not None:
            result_select = mfm.get_result_from_db(result_name=result_name)
            result_df = mfm.load_from_pickle(result_select.result_pickle)
            prediction_dict_list = mfm.transform_predict_result_to_dict_list(result_df)
            result_list = [{'id':result_select.id,'result_name':result_select.result_name}]+result_list
        else:
            result_df = mfm.load_from_pickle(result_row[0].result_pickle)
            prediction_dict_list = mfm.transform_predict_result_to_dict_list(result_df)

    return render_template(
        'prediction_loaded.html',alert_msg=alert_msg,
        prediction_list=prediction_dict_list,
        result_list=result_list
        )


# 테스트용!
@bp.route('/paper_loaded')
def paper_load_index():
    key_list = [
        {'k':'Identifier','v':'link_end'},
        {'k':'Abstract','v':'abstract'},
        {'k':'Title','v':'title'},
        {'k':'Keyword','v':'keyword'}
    ]

    paper_list =[]

    msg_code = request.args.get('msg_code', None)
    alert_msg = main_func.msg_processor(msg_code) if msg_code is not None else None
    
    # paper_route에서 온 load_key, value 확인
    load_key = request.args.get('load_key', None)
    load_value = request.args.get('load_value', None)
    
    if load_value == '':
        return 'Please Enter the value', 400
    
    # DB에서 현재 논문들 리스트를 불러와 출력
    if load_key == 'keyword':
        raw_paper_list = mfd.get_paper_filter_by_keyword(load_value)
    elif load_key == 'link_end':
        raw_paper_list = [mfd.get_paper_from_db(load_value)]
    else:
        raw_paper_list = mfd.get_paper_filter_like(load_key,load_value)

    if raw_paper_list:
        if raw_paper_list[0] is not None:
            for p in raw_paper_list:
                author_list = [p_a.one_author.name for p_a in p.many_paper_authors]
                keyword_list = [p_w.one_keyword.word for p_w in p.many_paper_keywords]
                paper_list.append({
                    "id":p.id,
                    "title":p.title,
                    "category":p.one_category.full_name,
                    "author":author_list,
                    "keyword":keyword_list,
                    "scites":p.scites,
                    "link_end":p.link_end,
                    "published_date":p.published_date,
                    "abstract":p.abstract
                    })
    elif load_value is not None:
        alert_msg = main_func.msg_processor(1)
    return render_template('paper_loaded.html', alert_msg=alert_msg, paper_list=paper_list,key_list=key_list)
