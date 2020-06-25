from flask import Flask, Blueprint, render_template, request
from flask_cors import CORS
import requests, json


bp_app = Blueprint('app', __name__, static_folder='static', static_url_path='/futuresynth/static', template_folder='templates')
bp_test = Blueprint('test', __name__, url_prefix='/futuresynth')


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


@bp_app.route('/execute_test_run', methods=['POST'])
def route_execute_test_run():
    test_conf = request.get_json()
    headers = {
        'Content-type': 'application/json'
    }

    res = json.loads(requests.post('http://127.0.0.1:4999/execute_test_run', data=json.dumps(test_conf), headers=headers).text)
    return res


@bp_app.route('/plan_test_run', methods=['POST'])
def route_plan_test_run():
    test_conf = request.get_json()
    headers = {
        'Content-type': 'application/json'
    }

    res = requests.post('http://127.0.0.1:4999/plan_test_run', data=json.dumps(test_conf), headers=headers).text
    return res


@bp_app.route('/delete_test', methods=['POST'])
def route_delete_test():
    test_conf = request.get_json()
    headers = {
        'Content-type': 'application/json'
    }

    res = requests.post('http://127.0.0.1:4999/delete_test', data=json.dumps(test_conf), headers=headers).text
    return res


@bp_app.route('/enable_test', methods=['POST'])
def route_enable_test():
    test_conf = request.get_json()
    headers = {
        'Content-type': 'application/json'
    }

    res = requests.post('http://127.0.0.1:4999/enable_test', data=json.dumps(test_conf), headers=headers).text
    return res


@bp_app.route('/check_name', methods=['GET'])
def route_check_name():
    entity_name = request.args.get('name')
    res = json.loads(requests.get('http://127.0.0.1:4999/check_name?name='+entity_name).text)
    print(res)
    return res

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(bp_app, url_prefix='/futuresynth')
    app.register_blueprint(bp_test, url_prefix='/futuresynth')
    return app
