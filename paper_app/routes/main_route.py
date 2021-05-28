from flask import Blueprint, render_template, request
from paper_app.utils import main_funcs
from paper_app.models.trained_model import Trained

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/compare', methods=["GET", "POST"])
def compare_index():

    raw_model_list = Trained.query.all()
    model_list = [{"model_name":model.model_name,"model_pkl":model.model_pkl} for model in raw_model_list]
    modelname, submit_x, x_row = "[ ____ ]","[ ____ ]","[ ____ ]"

    if request.method == "POST":
        request_data = request.form
        modelname = request_data["model_name"]
        x_row = request_data["row"]
        for model in model_list:
            if model['model_name'] == modelname:
                submit_x = model['model_pkl']['submit']['X'][int(x_row)]

    prediction = {"name":modelname, "submit_x":submit_x, "row":x_row}
    return render_template('compare_user.html', model_list=model_list, prediction=prediction)

@bp.route('/model/')
def model_index():
    """
    user_list 에 유저들을 담아 템플렛 파일에 넘겨주세요
    """

    msg_code = request.args.get('msg_code', None)
    
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None

    raw_model_list = Trained.query.all()
    model_list = [{"id":model.id, "model_name":model.model_name,"modle_pkl":model.model_pkl} for model in raw_model_list]

    return render_template('user.html', alert_msg=alert_msg, model_list=model_list)
