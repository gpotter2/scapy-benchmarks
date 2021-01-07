# scapy-benchmarks

### Dissection (IP+UDP+DNS) time

![Dissection](./build/dissects.png)

Lower is better

*Values are displayed RELATIVELY to the most recent mesure (the one on the right will always be 1.0)*

### Build (IP+UDP+DNS) time

![Build](./build/builds.png)

Lower is better

*Values are displayed RELATIVELY to the most recent mesure (the one on the right will always be 1.0)*

### Number of packet definitions

![Number of layers](./build/layers.png)

Note: Scada and automative layers are not included (too many "fake" layers)

### Number of contrib layers files

![Number of layers](./build/layers_mod.png)

### Infos

Host machine:
```
3.9.0 (default, Nov 12 2020, 22:22:02) 
[GCC 9.3.0]
```

Current master: [`210993d`](https://github.com/secdev/scapy/commit/210993d264b8779af6dee67f836352b961995924)
