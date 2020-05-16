from browsermobproxy import Server
from selenium import webdriver
import time, json, os, psutil


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../virtualenvs/app/Lib/site-packages/browsermobproxy/browsermob-proxy-2.1.4/bin/browsermob-proxy')


def run_selenium(test_conf, proxy, client):
    metrics = {}
    url = test_conf['url']

    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format(client.proxy))
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    navigation_timings = driver.execute_script("return performance.getEntriesByType('navigation')")
    # resource_timings = driver.execute_script("return performance.getEntriesByType('resource')")
    paint_timings = driver.execute_script("return performance.getEntriesByType('paint')")

    print(navigation_timings)

    metrics['connect_end'] = {'name': 'Connect End', 'value': round(navigation_timings[0]['connectEnd'], 2)}
    metrics['connect_start'] = {'name': 'Connect Start', 'value': round(navigation_timings[0]['connectStart'], 2)}
    metrics['dom_complete'] = {'name': 'DOM Complete', 'value': round(navigation_timings[0]['domComplete'], 2)}
    metrics['dom_content_loaded_event_end'] = {'name': 'DOM Content Loaded Event End', 'value': round(navigation_timings[0]['domContentLoadedEventEnd'], 2)}
    metrics['dom_content_loaded_event_start'] = {'name': 'DOM Content Loaded Event Start', 'value': round(navigation_timings[0]['domContentLoadedEventStart'], 2)}
    metrics['dom_interactive'] = {'name': 'DOM Interactive', 'value': round(navigation_timings[0]['domInteractive'], 2)}
    metrics['domain_lookup_end'] = {'name': 'Domain Lookup End', 'value': round(navigation_timings[0]['domainLookupEnd'], 2)}
    metrics['domain_lookup_start'] = {'name': 'Domain Lookup Start', 'value': round(navigation_timings[0]['domainLookupStart'], 2)}
    metrics['duration'] = {'name': 'Duration', 'value': round(navigation_timings[0]['duration'], 2)}
    metrics['fetch_start'] = {'name': 'Fetch Start', 'value': round(navigation_timings[0]['fetchStart'], 2)}
    metrics['load_event_end'] = {'name': 'Load Event End', 'value': round(navigation_timings[0]['loadEventEnd'], 2)}
    metrics['load_event_start'] = {'name': 'Load Event Start', 'value': round(navigation_timings[0]['loadEventStart'], 2)}
    # metrics['navigation_start'] = {'name': 'Load Event Start', 'value': round(navigation_timings[0]['navigationStart'], 2)}
    metrics['redirect_end'] = {'name': 'Redirect End', 'value': round(navigation_timings[0]['redirectEnd'], 2)}
    metrics['redirect_start'] = {'name': 'Redirect Start', 'value': round(navigation_timings[0]['redirectStart'], 2)}
    metrics['request_start'] = {'name': 'Request Start', 'value': round(navigation_timings[0]['requestStart'], 2)}
    metrics['response_end'] = {'name': 'Response End', 'value': round(navigation_timings[0]['responseEnd'], 2)}
    metrics['response_start'] = {'name': 'Response Start', 'value': round(navigation_timings[0]['responseStart'], 2)}
    metrics['secure_connection_start'] = {'name': 'Secure Connection Start', 'value': round(navigation_timings[0]['secureConnectionStart'], 2)}
    metrics['first_paint'] = {'name': 'First Paint', 'value': round(paint_timings[0]['startTime'], 2)}
    metrics['first_contentful_paint'] = {'name': 'First Contentful Paint', 'value': round(paint_timings[1]['startTime'], 2)}
    metrics['dns'] = {'name': 'DNS lookup', 'value': metrics['domain_lookup_end']-metrics['domain_lookup_start']}
    metrics['tcp_handshake'] = {'name': 'TCP Handshake', 'value': metrics['connect_end']-metrics['connect_start']}
    metrics['time_to_first_byte'] = {'name': 'Time to First Byte', 'value': metrics['response_start']-metrics['request_start']}
    metrics['ssl_negotiation'] = {'name': 'SSL negotiation', 'value': metrics['request_start']-metrics['secure_connection_start']}
    metrics['redirect_time'] = {'name': 'Redirect Time', 'value': metrics['redirect_end']-metrics['redirect_start']}


    time.sleep(3)

    har = json.dumps(client.har)
    return {'report': har, 'metrics': metrics, 'description': 'HAR'}


def terminate_browsermob():
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['name', 'cmdline'])
            if process_info.get('name') in ('java', 'java.exe'):
                for cmd_info in process_info.get('cmdline'):
                    if cmd_info == '-Dapp.name=browsermob-proxy':
                        process.kill()
        except psutil.NoSuchProcess:
            pass


# run_selenium({'url': 'https://www.google.com'})
# terminate_browsermob()
