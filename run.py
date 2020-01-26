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
    for cmd in [
        ["git", "fetch", "--prune-tags"],
        ["git", "reset", "--hard", "master"],
        ["git", "pull", "origin", "master"],
    ]:
        subprocess.Popen(
            cmd,
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
NB_LAYERS = []
NB_LAYERS_CONTRIB = []
NB_LAY_OK = []
NB_LAY_BRK = []

for tag in TAGS:
    print("Testing %s..." % tag)
    with open(os.devnull, "w") as dv:
        subprocess.Popen(
            ["git", "reset", "--hard", "--quiet", tag],
            cwd=pth,
            stdout=dv,
        ).communicate()
    if tag == "v2.2.0":
        extra = ["ikev2.py"]
    else:
        extra = []
    res = subprocess.Popen(
        [sys.executable, "test.py"] + extra,
        stdout=subprocess.PIPE
    ).communicate()[0].decode().strip().split("\n")[-1]
    parts = res.split(":")
    a, b = float(parts[0]), float(parts[1])
    c = map(int, parts[2].split(","))
    BUILDS.append(a)
    DISSECTS.append(b)
    NB_LAYERS.append(c[0])
    NB_LAYERS_CONTRIB.append(c[1])
    NB_LAY_OK.append(c[2])
    NB_LAY_BRK.append(c[3])

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

plt.bar(TAGS, NB_LAYERS_CONTRIB, label="contribs")
plt.bar(TAGS, NB_LAYERS, label="layers")
plt.legend()
plt.savefig("build/layers.png")
plt.clf()
os.chmod("build/layers.png", 0o777)

plt.bar(TAGS, NB_LAY_OK, label="contribs")
plt.bar(TAGS, NB_LAY_BRK, label="broken contribs")
plt.legend()
plt.savefig("build/layers_mod.png")
plt.clf()
os.chmod("build/layers_mod.png", 0o777)

# Rebuild README

with open("README.md.template") as fd:
    data = fd.read()
    data = data % (
        sys.version,
        master[:7], master
    )
    with open("README.md", "w") as out:
        out.write(data)
