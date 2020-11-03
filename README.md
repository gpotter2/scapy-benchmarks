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
3.9.0 (default, Oct  7 2020, 14:37:49) 
[GCC 9.3.0]
```

Current master: [`b'd6f0fd8'`](https://github.com/secdev/scapy/commit/b'd6f0fd8283f1bef90d570912caad5a8f8b476841')
