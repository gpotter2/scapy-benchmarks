"""
Run tests on all GH tags
"""

import os
import platform
import subprocess
import sys

if sys.version_info >= (3, 0, 0):
    raise OSError("Requires Python 2 to test Scapy < 2.4.0 !")

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

pth = os.path.abspath("./scapy")

# Prepare submodule

print("Fetching remote...")

with open(os.devnull, "w") as dv:
    subprocess.Popen(
        ["git", "fetch", "--prune-tags"],
        cwd=pth,
        stdout=dv,
    ).communicate()

master = subprocess.Popen(
    ["git", "rev-parse", "HEAD"],
    cwd=pth,
    stdout=subprocess.PIPE,
).communicate()[0].strip()

# Retrieve tags

TAGS = subprocess.Popen(
    ["git", "tag", "--list"],
    stdout=subprocess.PIPE,
    cwd=pth
).communicate()[0].decode().split()

TAGS = [
    x for x in TAGS if "rc" not in x and x[1] == "2"
]
TAGS = TAGS[TAGS.index("v2.2.0"):]
TAGS += ["master"]

# Perform tests

BUILDS = []
DISSECTS = []

for tag in TAGS:
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
    a, b = map(float, res.split(":"))
    BUILDS.append(a)
    DISSECTS.append(b)

# Re-scale

BUILDS = [x / BUILDS[-1] for x in BUILDS]
DISSECTS = [x / DISSECTS[-1] for x in DISSECTS]

# Graph

print("Exporting...")

try:
    os.mkdir("build")
except Exception:
    pass

plt.bar(TAGS, BUILDS)
plt.savefig("build/builds.png")
plt.clf()
os.chmod("build/builds.png", 0o777)

plt.bar(TAGS, DISSECTS)
plt.savefig("build/dissects.png")
plt.clf()
os.chmod("build/dissects.png", 0o777)

# Rebuild README

with open("README.md.template") as fd:
    data = fd.read()
    data = data % (
        sys.version,
        master[:7], master
    )
    with open("README.md", "w") as out:
        out.write(data)
