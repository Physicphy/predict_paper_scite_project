from flask import Blueprint, request, redirect, url_for, Response
from paper_app.utils import main_func

bp = Blueprint('paper', __name__)

mfd = main_func.data_func()

@bp.route('/paper', methods=['POST'])
def add_paper():
    request_data = request.form
    if not request_data:
        request_data = request.get_json()

    paper_dict_list = mfd.get_paper_dict_list_from_arxiv(
        key=request_data['key'],
        value=request_data['value'],
        keyword=request_data['keyword'],
        start_date=request_data['start_date'],
        end_date=request_data['end_date']
    )

    if paper_dict_list:
        mfd.add_all_from_dict_list(paper_dict_list)
        return redirect(url_for('main.paper_index',msg_code=0))
    else:
        return redirect(url_for('main.paper_index',msg_code=1))


@bp.route('/paper')
@bp.route('/paper/<link_end>')
def delete_paper(link_end=None):
    if link_end is None:
        return '',400
    elif mfd.get_paper_from_db(link_end) is not None:
        mfd.delete_paper(link_end)
        return redirect(url_for('main.paper_index', msg_code=2))
    else:
        return '',404


@bp.route('/paper_loaded', methods=['POST'])
def load_paper():
    request_data = request.form
    if not request_data:
        request_data = request.get_json()

    if request_data is not None:
        load_key = request_data['key']
        load_value = request_data['value']
        return redirect(url_for('main.paper_load_index',load_key=load_key,load_value=load_value))
    else:
        return redirect(url_for('main.paper_load_index'))

@bp.route('/paper_loaded')
@bp.route('/paper_loaded/<link_end>')
def delete_loaded_paper(link_end=None):
    if link_end is None:
        return '',400
    elif mfd.get_paper_from_db(link_end) is not None:
        mfd.delete_paper(link_end)
        return redirect(url_for('main.paper_load_index', msg_code=2))
    else:
        return '',404