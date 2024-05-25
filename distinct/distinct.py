import abc
import math
import random
import typing
from collections.abc import Iterable

T = typing.TypeVar("T")


class CountDistinct(abc.ABC):
    """Iterator to count the number of distinct elements in a stream."""

    def __init__(self, iterable: Iterable[T]):
        self.iter = iter(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        if element := next(self.iter):
            return self.step(element)
        raise StopIteration

    @abc.abstractmethod
    def step(self) -> int:
        """
        Compute the number of distinct elements in a stream so far given the
        next element in the stream.
        """

    def naive(iterable: Iterable[T]) -> "NaiveCountDistinct":
        return NaiveCountDistinct(iterable)

    def cvm(iterable: Iterable[T], capacity: int=100) -> "CvmCountDistinct":
        return CvmCountDistinct(iterable, capacity)


class NaiveCountDistinct(CountDistinct):
    """
    Naive approach to counting the number of distinct elements in a stream by
    adding all elements to a set and counting them.
    """
    def __init__(self, iterable: Iterable[T]):
        super().__init__(iterable)
        self.distincts = set()

    def step(self, element: T) -> int:
        self.distincts.add(element)
        return len(set(self.distincts))


class CvmCountDistinct(CountDistinct):
    """
    Estimate the number of distinct elements in a stream using the CVM
    algorithm.

    see: https://arxiv.org/abs/2301.10191
    """
    def __init__(self, iterable: Iterable[T], capacity: int=100):
        super().__init__(iterable)
        self.memory = set()
        self.capacity = capacity
        self.stage = 0

        assert capacity > 0, "capacity must be greater than zero"

    def step(self, element: T) -> int:
        if element in self.memory:
            self.memory.remove(element)

        # Add element (back) with probability p
        if random.random() < 1.0 / math.pow(2, self.stage):
            self.memory.add(element)

        # If threshold reached, remove all words with probability 1/2
        if len(self.memory) >= self.capacity:
            self.memory = {
                element for element in self.memory if random.random() < 0.5
            }
            self.stage += 1

            # The memory must not still be at threshold after removal step
            assert len(self.memory) != self.capacity, (
                "memory is still at capacity after removal step"
            )

        # estimate = |memory| / p, where p = 1 / 2^stage
        estimate = len(self.memory) * math.pow(2, self.stage)
        return round(estimate)
