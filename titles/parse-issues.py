#!/usr/bin/env python3

import os
import time
import requests
import json
import glob
import re


def read_json(issue_file):
    with open(issue_file, "r") as fd:
        content = json.loads(fd.read())
    return content


package_list = requests.get(
    "https://spack.github.io/packages/data/packages.json"
).json()
package_regex = "( %s )" % " | ".join(package_list)

# Keep track of issues we flag with packages, and those not
found = {}
missing = []

issue_files = os.listdir("data")

for issue_file in issue_files:

    try:
        issue = read_json(os.path.join("data", issue_file))
    except:
        print("Issue reading %s, skipping." % issue_file)
        continue
    title = " " + issue["title"].lower() + " "

    # Replace special characters
    title = re.sub("[!#%^*(){}:_&$+@\/\[\]]+", " ", title)

    # Any packages?
    packages = re.findall(package_regex, title)
    if not packages:
        missing.append(title)
    else:
        for pkg in packages:
            if pkg not in found:
                found[pkg] = []
            found[pkg].append(title)


# Save results to file
with open("matches.json", "w") as fd:
    fd.write(json.dumps(found, indent=4))
with open("misses.json", "w") as fd:
    fd.write(json.dumps(missing, indent=4))
