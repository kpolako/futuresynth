from flask import Flask, Blueprint, request, current_app
import os, json, influxdb
from flask_cors import CORS
from .audits import lighthouse_audit, selenium_audit, scheduler
from .conf import run_browsermob, influx_connector
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Boolean
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR


bp_app = Blueprint('app', __name__, static_folder='static')
bp_test = Blueprint('test', __name__)


#for quick checking if app and/or nginx is up and running
@bp_test.route('/health', methods=['GET'])
def route_test():
    return 'ok'


@bp_app.route('/get_confs', methods=['GET'])
def route_get_confs():
    Conf = current_app.config['Conf_class']
    table = Conf()
    res = table.return_all_list()
    return json.dumps(res)


@bp_app.route('/enable_test', methods=['POST'])
def route_enable_test():
    conf = request.get_json()
    print(conf)
    table_c = current_app.config['Conf_class']
    db = current_app.config['db']
    table_c.dis_enable_test(db, conf['test_name'], conf['enabled'])
    scheduler_obj = current_app.config['scheduler_obj']

    if conf['enabled']:
        res = table_c.return_object_dict(db, conf['test_name'])
        scheduler.schedule_job(current_app.config['scheduler_obj'], res,
                                                      kwargs={'client': current_app.config['client']})
        scheduler.schedule_job(scheduler_obj, res,
                               kwargs={'client': current_app.config['client']})
    else:
        jobs = scheduler_obj.get_jobs()
        for item in jobs:
            if item.name == conf['test_name']:
                scheduler_obj.remove_job(item.id)
            else:
                pass
        pass
    return 'ok'


@bp_app.route('/delete_test', methods=['POST'])
def route_delete_test():
    conf = request.get_json()
    print(conf)
    table_c = current_app.config['Conf_class']
    db = current_app.config['db']
    table_c.delete_test(db, conf['test_name'])
    return 'ok'


@bp_app.route('/check_name', methods=['GET'])
def route_check_entity_name():
    entity_name = request.args.get('name')
    print(entity_name)
    table_c = current_app.config['Conf_class']
    db = current_app.config['db']
    res = table_c.return_object_dict(db, entity_name)
    if res:
        return json.dumps({'exists': True})
    else:
        return json.dumps({'exists': False})


@bp_app.route('/plan_test_run', methods=['POST'])
def route_plan_test_run():
    test_conf = request.get_json()
    scheduler.schedule_job(current_app.config['scheduler_obj'], test_conf, kwargs={'client': current_app.config['client']})
    db = current_app.config['db']
    table = current_app.config['Conf_class']
    table.add_job_db(db, test_conf['name'], test_conf['url'], test_conf['device'], test_conf['type'],
                     test_conf['time_number'], test_conf['time_type'])
    return 'Test zaplanowany!'


@bp_app.route('/execute_test_run', methods=['POST'])
def route_execute_test_run():
    test_conf = request.get_json()
    result = None
    try:
        if test_conf['type'] == 'lighthouse':
            result = lighthouse_audit.run_lighthouse(test_conf)
        elif test_conf['type'] == 'selenium':
            result = selenium_audit.run_selenium_har(test_conf, current_app.config['client'])
    except Exception as e:
        result = {'error': 'Coś poszło nie tak!'}
    return result


def create_app():

    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(bp_app)
    app.register_blueprint(bp_test)

    influx_client = influxdb.InfluxDBClient(host='localhost', port=8086)

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../conf_database/confdb.db')

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+filename
    db = SQLAlchemy(app)

    scheduler_obj = BackgroundScheduler(daemon=True)

    class Conf(db.Model):
        __tablename__ = 'conf'

        id = Column(Integer, Sequence('conf_id_seq'), primary_key=True, nullable=False, autoincrement=True)
        name = Column(String(50), nullable=False, index=True, unique=True)
        url = Column(String(2048), nullable=False)
        device = Column(String(7), nullable=False)
        type = Column(String(10), nullable=False)
        time_number = Column(Integer, nullable=False)
        time_type = Column(String(1), nullable=False)
        created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
        enabled = Column(Boolean, nullable=False)

        def __repr__(self):
            return str(self.__dict__)

        def return_all_list(self):
            tb_list = self.query.all()
            res_list = []
            for item in tb_list:
                item.__dict__.pop('_sa_instance_state')
                ct = item.__dict__['created_date'].strftime("%m/%d/%Y, %H:%M:%S")
                item.__dict__.pop('created_date')
                item.__dict__['created_date'] = ct
                res_list.append(item.__dict__)
            return res_list

        @staticmethod
        def return_object_dict(db, name):
            obj = db.session.query(Conf.id, Conf.name, Conf.url, Conf.device, Conf.type, Conf.time_number,
                                   Conf.time_type, Conf.created_date, Conf.enabled).filter_by(name=name).first()
            if obj:
                obj_new = {'id': obj[0], 'name': obj[1], 'url': obj[2], 'device': obj[3], 'type': obj[4],
                           'time_number': obj[5],
                           'time_type': obj[6], 'created_date': obj[7].strftime("%m/%d/%Y, %H:%M:%S"), 'enable': obj[8]}
                return obj_new
            else:
                return None

        @staticmethod
        def add_job_db(db, name, url, device, type, time_number, time_type):
            conf = Conf(name=name, url=url, device=device,
                        type=type,
                        time_number=time_number, time_type=time_type, enabled=True)
            db.session.add(conf)
            db.session.commit()
            return 'job added'

        @staticmethod
        def dis_enable_test(db, name, value):
            db.session.query(Conf.id).filter_by(name=name).update(dict(enabled=value))
            db.session.commit()

        @staticmethod
        def delete_test(db, name):
            db.session.query(Conf.id).filter_by(name=name).delete()
            db.session.commit()

    db.create_all()

    proxy = run_browsermob.ProxyManager()
    proxy.start_server()
    client = proxy.start_client()
    client.new_har("options={'captureContent': True}")

    def test_exec_listener(event):
        if event.exception:
            return "crash"
        else:
            influx_connector.influx_connector(influx_client, event.retval)
            return 'ok'

    scheduler.run_jobs_from_db(scheduler_obj, client, Conf())
    scheduler_obj.start()
    scheduler_obj.add_listener(test_exec_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    with app.app_context():
        current_app.config['client'] = client
        current_app.config['scheduler_obj'] = scheduler_obj
        current_app.config['Conf_class'] = Conf
        current_app.config['db'] = db

    return app
