import subprocess, json

def run_lighthouse(test_conf):
    cc = 'lighthouse '+test_conf['url']+' --quiet --output=json'
    result = subprocess.check_output(cc, shell=True)
    res = json.loads(result)
    # with open('some.json', 'a') as f:
    #     f.write(json.dumps(res))
    return json.dumps(res)
