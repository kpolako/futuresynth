from flask import Flask, Blueprint, render_template
import logging, sys
from flask_cors import CORS
import requests, json


bp_app = Blueprint('app', __name__, static_folder='static')
bp_test = Blueprint('test', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False


#for quick checking if docker & nginx are up and running
@bp_test.route('/health', methods=['GET'])
def route_test():
    return 'ok'


@bp_app.route('/', methods=['GET'])
def route_home():
    return render_template('index.html')


@bp_app.route('/plan_test', methods=['GET'])
def route_plan_test():
    return render_template('plan.html')


@bp_app.route('/docs', methods=['GET'])
def route_docs():
    return render_template('docs.html')


@bp_app.route('/tests', methods=['GET'])
def route_all_tests():
    res = requests.get('http://127.0.0.1:4999/get_confs')
    return render_template('tests.html', tests=json.loads(res.text))


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(bp_app)
    app.register_blueprint(bp_test)
    return app
