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

# DEFINE TESTS

def test_ping(dest):
    pkt = []
    for i in range(1, 100):
        a = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=dest)
        pkt.append(a)
    ans, _ = srp(
        pkt,
        filter="host {0}".format(dest),
        inter=0,
        timeout=1,
        verbose=0
    )
    S = 0
    for pkt in ans:
        sent = pkt[0]
        received = pkt[1]
        S += (received.time - sent.sent_time) * 1000
    return S / len(ans)
import time

raw_packet = b'E\x00\x00(\x00\x01\x00\x00@\x11|\xc2\x7f\x00\x00\x01\x7f\x00\x00\x01\x005\x005\x00\x14\x00Z\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def test_dissect(N=1000):
    a = time.time()
    for i in range(N):
        IP(raw_packet)
    delta = time.time() - a
    return delta / N * 1000
import time

def test_build(N=1000):
    a = time.time()
    for i in range(N):
        IP(version=4, ihl=5, tos=0, len=40, id=1, flags=0, frag=0, ttl=64, proto=17, chksum=31938, src='127.0.0.1', dst='127.0.0.1')/UDP(sport=53, dport=53, len=20, chksum=90)/DNS()
    delta = time.time() - a
    return delta / N * 1000

# RUN TESTS

N = 1000
conf.route = Route()
ip = conf.route.route("0.0.0.0")[2]

a = test_build(N)
b = test_dissect(N)
c = test_ping(ip)

print("%s:%s:%s" % (a, b, c))
