from flask import Flask, Blueprint, request, render_template, current_app
import logging, sys
from flask_cors import CORS
from app.audits import lighthouse_audit, http_audit, selenium_audit
from app.conf import run_browsermob


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


@bp_app.route('/receive_test', methods=['POST'])
def route_receive_test():
    test_conf = request.get_json()
    print(test_conf)
    result = None
    if test_conf['type'] == 'lighthouse':
        result = lighthouse_audit.run_lighthouse(test_conf)
    elif test_conf['type'] == 'selenium':
        result = selenium_audit.run_selenium(test_conf, current_app.config['proxy'], current_app.config['client'])
        selenium_audit.terminate_browsermob()
    return result


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(bp_app)
    app.register_blueprint(bp_test)
    proxy = run_browsermob.ProxyManager()
    proxy.start_server()
    client = proxy.start_client()
    client.new_har("options={'captureContent': True}")
    with app.app_context():
        current_app.config['proxy'] = proxy
        current_app.config['client'] = client
    return app
