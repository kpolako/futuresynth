import influxdb
from datetime import datetime


# client = influxdb.InfluxDBClient(host='localhost', port=8086)
# client.create_database('performance-lighthouse')
# client.create_database('performance-selenium')
# client.create_database('performance-http')
# client.create_database('futuresynth')
# print(client.get_list_database())

test = {
    'test_conf': {
        'name': 'somename',
        'url': 'https://google.com',
        'device': 'mobile',
        'type': 'selenium',
        'time_number': 1,
        'time_type': 'm'
    },
    'metrics': {
        'first_paint': 444,
        'first_contentful_paint': 555,
        'dns_lookup': 20
    }
}


# for item in test['metrics']:
#     print(item, ': ', test['metrics'][item])



# def influx_connector(test, client):
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
    print(data_point)
    points.append(data_point)
    print(data_point)
    res = client.write_points(points=points)
    return 'ok'


# influx_connector(test)