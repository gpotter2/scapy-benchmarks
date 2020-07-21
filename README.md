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
2.7.18 (default, Jul 21 2020, 17:54:49) 
[GCC 9.3.0]
```

Current master: [`6926301`](https://github.com/secdev/scapy/commit/69263018215a93731ecc5cb1a30b63ed07acd72b)
