import subprocess, json


def run_lighthouse(test_conf):
    metrics = {}
    cc = 'lighthouse '+test_conf['url']+' --port=9222 --quiet --emulated-form-factor '+test_conf['device']+' --only-categories=performance --output=json'
    result_json = subprocess.check_output(cc, shell=True)
    result_dict = json.loads(result_json)
    result_dict_audits = result_dict['audits']
    result_dict_metrics = result_dict_audits['metrics']['details']['items'][0]

    try:
        metrics['first_contentful_paint'] = {'name': 'First Contentful Paint', 'value': round(result_dict_audits['first-contentful-paint']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['first_meaningful_paint'] = {'name': 'First Meaningful Paint', 'value': round(result_dict_audits['first-meaningful-paint']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['speed_index'] = {'name': 'Speed Index', 'value': round(result_dict_audits['speed-index']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['estimated_input_latency'] = {'name': 'Estimated Input Latency', 'value': round(result_dict_audits['estimated-input-latency']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['max_potential_first_input_delay'] = {'name': 'Max Potential First Input Delay', 'value': round(result_dict_audits['max-potential-fid']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['time_to_first_byte'] = {'name': 'Time to First Byte', 'value': round(result_dict_audits['server-response-time']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['first_cpu_idle'] = {'name': 'First CPU Idle', 'value': round(result_dict_audits['first-cpu-idle']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['time_to_interactive'] = {'name': 'Time to Interactive', 'value': round(result_dict_audits['interactive']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['round_trip_time'] = {'name': 'Round Trip Time', 'value': round(result_dict_audits['network-rtt']['numericValue'], 2)}
    except:
        pass

    try:
        metrics['largest_contentful_paint'] = {'name': 'Largest Contentful Paint', 'value': round(result_dict_metrics['observedLargestContentfulPaint'], 2)}
    except:
        pass

    try:
        metrics['first_paint'] = {'name': 'First Paint', 'value': round(result_dict_metrics['observedFirstPaint'], 2)}

    except:
        pass

    try:
        metrics['dom_content_loaded'] = {'name': 'DOM Content Loaded', 'value': round(result_dict_metrics['observedDomContentLoaded'], 2)}
    except:
        pass

    try:
        metrics['lighthouse_performance_score'] = {'name': 'Lighthouse Performance Score', 'value': round(result_dict['categories']['performance']['score'], 2)*100}
    except:
        pass

    return {'report': json.dumps(result_dict), 'metrics': metrics, 'description': 'Lighthouse', 'test_conf': test_conf}
