import requests


def run_request(test_conf):
    response = requests.get(test_conf['url'])
    return {'status_code': response.status_code, 'test_conf': test_conf}

# run_request('https://www.stepstone.de')
