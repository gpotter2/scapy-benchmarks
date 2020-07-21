"""
Run tests on all GH tags
"""

from __future__ import print_function

import argparse
import os
import platform
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

pth = os.path.abspath("./scapy")

# Handle command line

parser = argparse.ArgumentParser()
parser.add_argument('references', metavar='refs', type=str, nargs='*',
                    help='git references to compare')
args = parser.parse_args()

# Prepare submodule

print("Fetching remote... ", end="")

with open(os.devnull, "w") as dv:
    for cmd in [
        ["git", "fetch", "--prune-tags", "--quiet"],
        ["git", "reset", "--hard", "master", "--quiet"],
        ["git", "pull", "origin", "master", "--quiet"],
    ]:
        err = subprocess.Popen(
            cmd,
            cwd=pth,
            stdout=dv,
            stderr=subprocess.PIPE,
        ).communicate()[1]
        if err:
            print("ERROR")
            print(err)
            sys.exit(1)

master = subprocess.Popen(
    ["git", "rev-parse", "HEAD"],
    cwd=pth,
    stdout=subprocess.PIPE,
).communicate()[0].strip()

print("OK")

# Retrieve tags

if args.references:
    TAGS = args.references
else:
    if sys.version_info >= (3, 0, 0):
        raise OSError("Requires Python 2 to test Scapy < 2.4.0 !")

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
NB_LAYERS_NONDEFAULT = []
NB_LAYERS_CONTRIB = []
NB_LAY_OK = []
NB_LAY_BRK = []

for tag in TAGS:
    print("Testing %s:" % tag)
    # CHECKOUT
    print("  checkout... ", end="")
    with open(os.devnull, "w") as dv:
        err = subprocess.Popen(
            ["git", "reset", "--hard", "--quiet", tag],
            cwd=pth,
            stdout=dv,
            stderr=subprocess.PIPE
        ).communicate()[1]
    if err:
        print("ERROR")
        print(err.decode())
    else:
        print("OK")
    # TESTING
    print("  running test... ", end="")
    if tag == "v2.2.0":
        extra = ["ikev2.py"]
    else:
        extra = []
    res = subprocess.Popen(
        [sys.executable, "test.py"] + extra,
        stdout=subprocess.PIPE
    ).communicate()[0].decode().strip().split("\n")[-1]
    try:
        parts = res.split(":")
        a, b = float(parts[0]), float(parts[1])
        c = list(map(int, parts[2].split(",")))
        BUILDS.append(a)
        DISSECTS.append(b)
        NB_LAYERS.append(c[0])
        NB_LAYERS_NONDEFAULT.append(c[1])
        NB_LAYERS_CONTRIB.append(c[2])
        NB_LAY_OK.append(c[3])
        NB_LAY_BRK.append(c[4])
    except Exception:
        print("ERROR")
    else:
        print("OK")

# Re-scale

BUILDS = [x / BUILDS[-1] for x in BUILDS]
DISSECTS = [x / DISSECTS[-1] for x in DISSECTS]

# Variation

VARIATIONS_BUILDS = ["{:+.2%}".format(x - 1) for x in BUILDS]
VARIATIONS_DISSECTS = ["{:+.2%}".format(x - 1) for x in DISSECTS]

VARIATIONS_BUILDS[-1] = ""
VARIATIONS_DISSECTS[-1] = ""

# Graph

print("Exporting... ", end="")

def label_bar(bar, labels):
    """Add a label above each bar"""
    i = 0
    for rect in bar:
        lbl = labels[i]
        i += 1
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, lbl, ha='center', va='bottom')

try:
    os.mkdir("build")
except Exception:
    pass

bar = plt.bar(TAGS, BUILDS)
label_bar(bar, VARIATIONS_BUILDS)
plt.savefig("build/builds.png")
plt.clf()
os.chmod("build/builds.png", 0o777)

bar = plt.bar(TAGS, DISSECTS)
label_bar(bar, VARIATIONS_DISSECTS)
plt.savefig("build/dissects.png")
plt.clf()
os.chmod("build/dissects.png", 0o777)

plt.bar(TAGS, NB_LAYERS_CONTRIB, label="contribs")
plt.bar(TAGS, NB_LAYERS, label="layers")
plt.bar(TAGS, NB_LAYERS_NONDEFAULT, label="non default layers")
plt.legend()
plt.savefig("build/layers.png")
plt.clf()
os.chmod("build/layers.png", 0o777)

plt.bar(TAGS, NB_LAY_OK, label="layers/contribs")
plt.bar(TAGS, NB_LAY_BRK, label="broken layers/contribs")
plt.legend()
plt.savefig("build/layers_mod.png")
plt.clf()
os.chmod("build/layers_mod.png", 0o777)

print("OK")

# Rebuild README

print("Rebuilding readme... ", end="")

with open("README.md.template") as fd:
    data = fd.read()
    data = data % (
        sys.version,
        master[:7], master
    )
    with open("README.md", "w") as out:
        out.write(data)

print("OK")
