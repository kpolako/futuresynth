from backend_app.audits import http_audit, lighthouse_audit, selenium_audit


def schedule_job(scheduler_obj, test_conf, **kwargs):
    job = None
    if test_conf['type'] == 'selenium':
        if test_conf['time_type'] == 's':
            job = scheduler_obj.add_job(selenium_audit.run_selenium_har, 'interval', name=test_conf['name'], seconds=test_conf['time_number'],
                                    args=[test_conf, kwargs['kwargs']['client']])
        elif test_conf['time_type'] == 'm':
            job = scheduler_obj.add_job(selenium_audit.run_selenium_har, 'interval', name=test_conf['name'], minutes=test_conf['time_number'],
                                    args=[test_conf, kwargs['kwargs']['client']])
        elif test_conf['time_type'] == 'h':
            job = scheduler_obj.add_job(selenium_audit.run_selenium_har, 'interval', name=test_conf['name'], hours=test_conf['time_number'],
                                    args=[test_conf, kwargs['kwargs']['client']])

    elif test_conf['type'] == 'lighthouse':
        if test_conf['time_type'] == 's':
            job = scheduler_obj.add_job(lighthouse_audit.run_lighthouse, 'interval', name=test_conf['name'], seconds=test_conf['time_number'], args=[test_conf])
        elif test_conf['time_type'] == 'm':
            job = scheduler_obj.add_job(lighthouse_audit.run_lighthouse, 'interval', name=test_conf['name'], minutes=test_conf['time_number'], args=[test_conf])
        elif test_conf['time_type'] == 'h':
            job = scheduler_obj.add_job(lighthouse_audit.run_lighthouse, 'interval', name=test_conf['name'], hours=test_conf['time_number'], args=[test_conf])
    elif test_conf['type'] == 'http':
        if test_conf['time_type'] == 's':
            job = scheduler_obj.add_job(http_audit.run_request, 'interval', name=test_conf['name'], seconds=test_conf['time_number'], args=[test_conf])
        elif test_conf['time_type'] == 'm':
            job = scheduler_obj.add_job(http_audit.run_request, 'interval', name=test_conf['name'], minutes=test_conf['time_number'], args=[test_conf])
        elif test_conf['time_type'] == 'h':
            job = scheduler_obj.add_job(http_audit.run_request, 'interval', name=test_conf['name'], hours=test_conf['time_number'], args=[test_conf])
    else:
        return 'wrong test type'
    print(job)
    return 'ok'


def run_jobs_from_db(scheduler_obj, client, table):
    result = table.query.all()
    for item in result:
        if item.__dict__['enabled']:
            schedule_job(scheduler_obj, item.__dict__, kwargs={'client': client})
        else:
            pass

