#!/usr/bin/env python3

import os
import time
import requests
import json

token = os.environ.get('GITHUB_TOKEN')
headers = {"Authentication": "token %s" % token, "Accept": "application/vnd.github.v3+json"}

# Get open and closed issues
url = "https://api.github.com/repos/spack/spack/issues?filter=all&state=all&per_page=100&page="

# make issues output folder
if not os.path.exists("data"):
    os.makedirs("data")

# "application/vnd.github.VERSION.full+json
next_page = 1
while next_page:
    print("Parsing page %s" % next_page)

    response = requests.get(url + str(next_page), headers=headers)
    while response.reason == "rate limit exceeded":
        print("Sleeping 10 minutes...")
        time.sleep(600)
        response = requests.get(url + str(next_page), headers=headers)

    results = None
    if response.status_code == 200:
        results = response.json()
        for issue in results:
            outfile = os.path.join("data", str(issue['number']) + ".json")
            if os.path.exists(outfile):
                continue
            with open(outfile, 'w') as fd:
                fd.writelines(json.dumps(issue, indent=4))

    if not results:
        next_page = None
        break
    next_page +=1
    
