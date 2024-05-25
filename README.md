# distinct

Demonstrating count-distinct algorithms on streaming data.

The counters are implemented as iterators which take an
iterable and return the distinct count so far given the next value in the iterable each time next is called.

Currently uses naive and [CVM](https://arxiv.org/abs/2301.10191) algorithms but may also add HyperLogLog in the future.

## Usage

```
(env) $ python3 -m distinct naive
INFO:distinct.cli:Found 63149 distinct elements in 159.40 seconds using naive algorithm
(env) $ python3 -m distinct cvm
INFO:distinct.cli:Found 50176 distinct elements in 0.07 seconds using cvm algorithm
(env) $ python3 -m distinct cvm --capacity 1000
INFO:distinct.cli:Found 61440 distinct elements in 0.08 seconds using cvm algorithm
```
