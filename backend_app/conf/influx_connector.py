from datetime import datetime


def influx_connector(client, test):
    points = []
    client.switch_database('futuresynth')
    t_now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    tags = {
        'name': test['test_conf']['name'],
        'url': test['test_conf']['url'],
        'device': test['test_conf']['device'],
    }
    fields = {}

    if test['test_conf']['type'] == 'http':
        fields['status'] = test['status_code']
    else:
        for item in test['metrics']:
            fields[item] = int(test['metrics'][item]['value'])

    data_point = {
            "measurement": test['test_conf']['type'],
            "tags": tags,
            "time": t_now,
            "fields": fields
        }
    points.append(data_point)
    res = client.write_points(points=points)
    return 'ok'
