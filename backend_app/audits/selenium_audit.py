from selenium import webdriver
import time, json, os, psutil, atexit


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../virtualenvs/app/Lib/site-packages/browsermobproxy/browsermob-proxy-2.1.4/bin/browsermob-proxy')


def run_selenium_har(test_conf, client):
    metrics = {}
    url = test_conf['url']

    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "iPhone 6 Plus"}
    options.add_argument("--proxy-server={}".format(client.proxy))
    options.add_argument('--ignore-certificate-errors')
    if test_conf['device'] == 'mobile':
        options.add_experimental_option("mobileEmulation", mobile_emulation)
    else:
        pass
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    navigation_timings = driver.execute_script("return performance.getEntriesByType('navigation')")
    # resource_timings = driver.execute_script("return performance.getEntriesByType('resource')")
    paint_timings = driver.execute_script("return performance.getEntriesByType('paint')")

    # print(navigation_timings)

    metrics['connect_end'] = {'name': 'Connect End', 'type': 'timing_marks', 'value': round(navigation_timings[0]['connectEnd'], 2)}
    metrics['connect_start'] = {'name': 'Connect Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['connectStart'], 2)}
    metrics['dom_complete'] = {'name': 'DOM Complete', 'type': 'timing_marks', 'value': round(navigation_timings[0]['domComplete'], 2)}
    metrics['dom_content_loaded_event_end'] = {'name': 'DOM Content Loaded Event End', 'type': 'timing_marks', 'value': round(navigation_timings[0]['domContentLoadedEventEnd'], 2)}
    metrics['dom_content_loaded_event_start'] = {'name': 'DOM Content Loaded Event Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['domContentLoadedEventStart'], 2)}
    metrics['dom_interactive'] = {'name': 'DOM Interactive', 'type': 'timing_marks', 'value': round(navigation_timings[0]['domInteractive'], 2)}
    metrics['domain_lookup_end'] = {'name': 'Domain Lookup End', 'type': 'timing_marks', 'value': round(navigation_timings[0]['domainLookupEnd'], 2)}
    metrics['domain_lookup_start'] = {'name': 'Domain Lookup Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['domainLookupStart'], 2)}
    metrics['duration'] = {'name': 'Duration', 'type': 'timing_marks', 'value': round(navigation_timings[0]['duration'], 2)}
    metrics['fetch_start'] = {'name': 'Fetch Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['fetchStart'], 2)}
    metrics['load_event_end'] = {'name': 'Load Event End', 'type': 'timing_marks', 'value': round(navigation_timings[0]['loadEventEnd'], 2)}
    metrics['load_event_start'] = {'name': 'Load Event Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['loadEventStart'], 2)}
    metrics['redirect_end'] = {'name': 'Redirect End', 'type': 'timing_marks', 'value': round(navigation_timings[0]['redirectEnd'], 2)}
    metrics['redirect_start'] = {'name': 'Redirect Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['redirectStart'], 2)}
    metrics['request_start'] = {'name': 'Request Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['requestStart'], 2)}
    metrics['response_end'] = {'name': 'Response End', 'type': 'timing_marks', 'value': round(navigation_timings[0]['responseEnd'], 2)}
    metrics['response_start'] = {'name': 'Response Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['responseStart'], 2)}
    metrics['secure_connection_start'] = {'name': 'Secure Connection Start', 'type': 'timing_marks', 'value': round(navigation_timings[0]['secureConnectionStart'], 2)}
    metrics['first_paint'] = {'name': 'First Paint', 'type': 'paint_metrics', 'value': round(paint_timings[0]['startTime'], 2)}
    metrics['first_contentful_paint'] = {'name': 'First Contentful Paint', 'type': 'paint_metrics', 'value': round(paint_timings[1]['startTime'], 2)}
    metrics['dns'] = {'name': 'DNS lookup', 'type': 'calculated', 'value': round(metrics['domain_lookup_end']['value']-metrics['domain_lookup_start']['value'], 2)}
    metrics['tcp_handshake'] = {'name': 'TCP Handshake', 'type': 'calculated', 'value': round(metrics['connect_end']['value']-metrics['connect_start']['value'], 2)}
    metrics['time_to_first_byte'] = {'name': 'Time to First Byte', 'type': 'calculated', 'value': round(metrics['response_start']['value']-metrics['request_start']['value'], 2)}
    metrics['ssl_negotiation'] = {'name': 'SSL negotiation', 'type': 'calculated', 'value': round(metrics['request_start']['value']-metrics['secure_connection_start']['value'], 2)}
    metrics['redirect_time'] = {'name': 'Redirect Time', 'type': 'calculated', 'value': round(metrics['redirect_end']['value']-metrics['redirect_start']['value'], 2)}


    # time.sleep(3)

    har = json.dumps(client.har)
    driver.close()
    return {'report': har, 'metrics': metrics, 'description': 'HAR', 'test_conf': test_conf}


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
