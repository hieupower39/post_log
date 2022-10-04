#!/usr/bin/env python3
import requests
import sys
import getopt
import warnings

def ajiant_post_event(data='{'+'}'):
    url = 'https://ajiant.com/correlation/DebugTest'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'Authorization':'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImhpZXVuYyIsImV4cCI6MTY2NDkzNDI1NX0.gNIRJRpgSup3-soroelipVGW3W0Em_mIEq6TWALK9AaPwMKskhcNrwQA9HIX98h4cHdqy4-fWtZL9T-JY9139DqgH9q2Zg4HIgC7038F8-cWsYXBtc_ThgCzg_e6aW7_fFncB6w_oqqavcH4AvElnCawcmir9aFDHJz1_TvZXyElC7AYEGKUPQsivS7QtfLF8b4na-In-wQCGMYDEuE7pAX4lu_YqTtXWP7xZLceKdaTZrgYkd2MQc7O9ooYiZIAhp3hah8s64jXNCos1C5XX40RhGGeJ13F75bZ4VZXT-S1sCtk3-7z43ms8pZd0ieHrcrpBs1WorBU_REVdwnVhA'
    }

    req = requests.post(url=url, headers=headers, data=data,verify=False)
    return req

def print_result(req):
    print(str(req.status_code)+" "+req.reason)
    for key, value in req.headers.items():
        print(key+": "+value)
    print("\n")
    print(req.text)

    
def main(argv):
    warnings.filterwarnings("ignore")
    input_file = ''
    opts, args = getopt.getopt(argv,"hr:o:",["json_file="])
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -r <json_file>')
            sys.exit()
        if opt == '-r':
             input_file = arg
    req = ajiant_post_event(data=open(input_file, 'rb'))
    print_result(req)

if __name__ == "__main__":
    main(sys.argv[1:])
        
