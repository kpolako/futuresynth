import requests


def run_request(url):
    response = requests.get(url)
    return {'status_code': response.status_code}

# run_request('https://www.stepstone.de')
