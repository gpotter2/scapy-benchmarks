"""
Run tests on all GH tags
"""

import os
import subprocess
import sys

pth = os.path.abspath("./scapy")

tags = subprocess.Popen(
    ["git", "tag", "--list"],
    stdout=subprocess.PIPE,
    cwd=pth
).communicate()[0].decode().split()

tags = [
    x for x in tags if "rc" not in x and x[1] == "2"
]
tags = tags[tags.index("v2.2.0"):]

print(tags)

for tag in tags:
    print("Testing %s..." % tag)
    with open(os.devnull, "w") as dv:
        subprocess.Popen(
            ["git", "checkout", "--quiet", tag],
            cwd=pth,
            stdout=dv,
        ).communicate()
    res = subprocess.Popen(
        [sys.executable, "test.py"],
        stdout=subprocess.PIPE
    ).communicate()[0].decode()
    a, b, c = map(float, res.split(":"))
    print(a, b, c)
