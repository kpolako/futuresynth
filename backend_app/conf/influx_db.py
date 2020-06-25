import influxdb


def create_influx_db():
    client = influxdb.InfluxDBClient(host='localhost', port=8086)
    client.create_database('futuresynth')
    print(client.get_list_database())


# create_influx_db()