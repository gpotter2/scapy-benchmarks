"""
Performs benchmarking for the current version
"""

import os
import sys
sys.path.append(os.path.abspath("./scapy"))
sys.path.append(os.path.abspath("./scapy/scapy"))
sys.path.append(os.path.abspath("./scapy/scapy/layers"))

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy").setLevel(logging.ERROR)

from scapy.all import *

import importlib
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
        bytes(IP(version=4, ihl=5, tos=0, len=40, id=1, flags=0, frag=0, ttl=64, proto=17, chksum=31938, src='127.0.0.1', dst='127.0.0.1')/UDP(sport=53, dport=53, len=20, chksum=90)/DNS())
    delta = time.time() - a
    return delta / N * 1000

def nb_layers():
    lay_default = len(conf.layers)
    # Load contribs
    def _load(ty):
        lay_init = len(conf.layers)
        nb_ok = 0
        nb_broken = 0
        for fname in os.listdir("scapy/scapy/%s" % ty):
            # We dont want to include automaton or scada
            # (too many "fake" layers)
            if fname.endswith('.py'):
                try:
                    if fname in sys.argv:
                        raise Exception
                    importlib.import_module(
                        "scapy.%s.%s" % (ty, fname[:-3])
                    )
                    nb_ok += 1
                except Exception:
                    nb_broken += 1
        return (len(conf.layers) - lay_init), nb_ok, nb_broken
    lay_lay, nb_lay_ok, nb_lay_broken = _load("layers")
    lay_contrib, nb_contrib_ok, nb_contrib_broken = _load("contrib")
    nb_contrib_ok += nb_lay_ok
    nb_contrib_broken += nb_lay_broken
    return ",".join(str(x) for x in [
               lay_default, lay_lay, lay_contrib,
               nb_contrib_ok, nb_contrib_broken
           ])

# RUN TESTS

N = 20000

a = test_build(N)
b = test_dissect(N)
c = nb_layers()

print("%s:%s:%s" % (a, b, c))
