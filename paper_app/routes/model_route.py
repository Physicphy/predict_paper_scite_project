from flask import Blueprint, request, redirect, url_for, Response
from paper_app.models import user_model, paper_model, trained_model
import pickle

bp = Blueprint('model', __name__)

@bp.route('/model', methods=['POST'])
def add_model():
    request_data = request.form
    model_name = request_data['model_name']
    file_name = 'paper_app/KAERI_lgb_model.pickle'
    with open(file_name, 'rb') as f:
        loaded_model = pickle.load(f)
    trained_model.add_model(model_name,loaded_model)

    return redirect(url_for('main.model_index', msg_code=0))
        
@bp.route('/model/')
@bp.route('/model/<model_name>')
def delete_model(model_name=None):

    if model_name is None:
        return '',400

    delete_model_result = trained_model.delete_model(model_name)
    if delete_model_result:
        return redirect(url_for('main.model_index', msg_code=3))
    else:
        return '',404
