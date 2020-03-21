from __future__ import annotations

import itertools
import math
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Tuple

DICE_INPUT_FMT = re.compile(r"^\s*(?P<n_dice>\d+)d(?P<n_face>\d+)\s*$")


@dataclass
class DiceRoll:
    n_face: int
    n_dice: int

    def n_permutations(self, x: int) -> int:
        return _perms(x, self.n_dice, self.n_face)

    def prob(self, x: int) -> float:
        return self.n_permutations(x) / self.size_outcomes

    def prob_range(self, xs: Iterable[int]) -> float:
        return sum(self.n_permutations(x) for x in xs) / self.size_outcomes

    def prob_leq(self, x: int) -> float:
        if x <= self.mean:
            return self.prob_range(range(self.min, x + 1))
        return 1 - self.prob_range(range(x, self.max + 1))

    def prob_geq(self, x: int) -> float:
        if x >= self.mean:
            return self.prob_range(range(x, self.max + 1))
        return 1 - self.prob_range(range(self.min, x + 1))

    def possible_outcomes(self) -> Iterable[int]:
        yield from range(self.min, self.max + 1)

    @property
    def mean(self) -> float:
        return (self.max - self.min) / 2 + self.min

    @property
    def min(self) -> int:
        return self.n_dice

    @property
    def max(self) -> int:
        return self.n_dice * self.n_face

    @property
    def size_outcomes(self) -> int:
        return self.n_face ** self.n_dice

    @classmethod
    def parse(cls, input_str: str) -> Optional[DiceRoll]:
        if (match := DICE_INPUT_FMT.match(input_str)) is not None:
            n_face, n_dice = (int(match.group(g)) for g in ("n_face", "n_dice"))
            return cls(n_face=n_face, n_dice=n_dice)


def _perms(z: int, x: int, y: int) -> int:
    result = 0
    for i in range(math.floor((z - x) / y) + 1):
        j = z - x - i * y
        result += binomial_coeff(x, i) * neg_binomial_coeff(x, j) * even(i) * even(j)
    return result


def even(n: int) -> int:
    return 1 if (n % 2 == 0) else -1


@lru_cache(maxsize=2 ** 12)
def binomial_coeff(n: int, k: int) -> int:
    if not (0 <= k <= n):
        return 0
    result = 1
    for i in range(min(k, n - k)):
        result *= n - i
        result //= i + 1
    return result


def neg_binomial_coeff(n: int, k: int) -> int:
    return even(k) * binomial_coeff(n + k - 1, k)
