"""
Performs benchmarking for the current version
"""

import os
import sys
sys.path.append(os.path.abspath("./scapy"))
sys.path.append(os.path.abspath("./scapy/scapy"))

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy").setLevel(logging.ERROR)

from scapy.all import *

import imp
import os

# DEFINE TESTS

import time

raw_packet = b'E\x00\x00(\x00\x01\x00\x00@\x11|\xc2\x7f\x00\x00\x01\x7f\x00\x00\x01\x005\x005\x00\x14\x00Z\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def test_dissect(N=5000):
    a = time.time()
    for i in range(N):
        IP(raw_packet)
    delta = time.time() - a
    return delta / N * 1000
import time

def test_build(N=5000):
    a = time.time()
    for i in range(N):
        IP(version=4, ihl=5, tos=0, len=40, id=1, flags=0, frag=0, ttl=64, proto=17, chksum=31938, src='127.0.0.1', dst='127.0.0.1')/UDP(sport=53, dport=53, len=20, chksum=90)/DNS()
    delta = time.time() - a
    return delta / N * 1000

def nb_layers():
    lay_default = len(conf.layers)
    # Load contribs
    nb_contrib_ok = 0
    nb_contrib_broken = 0
    for fname in os.listdir("scapy/scapy/contrib"):
        # We dont want to include automaton or scada
        # (too many "fake" layers)
        if fname.endswith('.py'):
            try:
                if fname in sys.argv:
                    raise Exception
                imp.load_source("null", os.path.abspath(
                    os.path.join(
                        "scapy/scapy/contrib/",
                        fname
                    )
                ))
                nb_contrib_ok += 1
            except Exception:
                nb_contrib_broken += 1
    lay_contrib = len(conf.layers) - lay_default
    return ",".join(str(x) for x in [
               lay_default, lay_contrib,
               nb_contrib_ok, nb_contrib_broken
           ])

# RUN TESTS

N = 5000

a = test_build(N)
b = test_dissect(N)
c = nb_layers()

print("%s:%s:%s" % (a, b, c))
