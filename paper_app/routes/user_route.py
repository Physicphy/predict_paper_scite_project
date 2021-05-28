from flask import Blueprint, request, redirect, url_for, Response
from paper_app.models import user_model, paper_model, trained_model
import pickle

bp = Blueprint('user', __name__)

@bp.route('/model', methods=['POST'])
def add_model():
    file_name = 'KAERI_lgb_model.pickle'
    with open(file_name, 'rb') as f:
        loaded_model = pickle.load(f)
    trained_model.add_model('test_model',loaded_model)

    return redirect(url_for('main.user_index', msg_code=0))
        
@bp.route('/model/')
@bp.route('/model/<str:model_name>')
def delete_model(model_name=None):

    if model_name is None:
        return '',400

    delete_model_result = trained_model.delete_model(model_name)
    if delete_model_result:
        return redirect(url_for('main.user_index', msg_code=3))
    else:
        return '',404
