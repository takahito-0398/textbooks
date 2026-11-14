"""Finite Aztec diamonds, independent enumeration, and domino shuffling.

Cells use integer lower-left corners; their centers are (i+1/2,j+1/2).
The order-dependent coloring below is part of the shuffling contract.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product
from random import Random

Cell = tuple[int, int]
Domino = tuple[Cell, Cell]
Tiling = tuple[Domino, ...]


def cells(order: int) -> frozenset[Cell]:
    if not isinstance(order, int) or order < 0:
        raise ValueError("order must be a nonnegative integer")
    return frozenset((i, j) for i in range(-order, order)
                     for j in range(-order, order)
                     if abs(2*i+1) + abs(2*j+1) <= 2*order)


def canonical(dominoes) -> Tiling:
    return tuple(sorted(tuple(sorted(domino)) for domino in dominoes))


def validate_tiling(order: int, tiling: Tiling) -> None:
    covered = [cell for domino in tiling for cell in domino]
    if len(covered) != len(set(covered)) or set(covered) != cells(order):
        raise ValueError("tiling must cover exactly the diamond without overlap")
    if any(len(domino) != 2 or sum(abs(a-b) for a, b in zip(*domino)) != 1
           for domino in tiling):
        raise ValueError("domino cells must share one edge")


def enumerate_tilings(order: int) -> tuple[Tiling, ...]:
    """Exact matching search, deliberately independent of shuffling."""
    def visit(remaining):
        if not remaining:
            yield ()
            return
        i, j = min(remaining)
        for neighbor in ((i+1, j), (i, j+1)):
            if neighbor in remaining:
                for tail in visit(remaining - {(i, j), neighbor}):
                    yield (((i, j), neighbor),) + tail
    return tuple(canonical(tiling) for tiling in visit(cells(order)))


def matching_count(order: int) -> int:
    """Count by memoized occupancy masks, without the enumeration formula."""
    ordered = sorted(cells(order))
    indices = {cell: index for index, cell in enumerate(ordered)}
    neighbors = [[indices[p] for p in ((i+1, j), (i, j+1)) if p in indices]
                 for i, j in ordered]

    @lru_cache(None)
    def count(mask):
        if not mask:
            return 1
        first = (mask & -mask).bit_length()-1
        return sum(count(mask ^ (1 << first) ^ (1 << neighbor))
                   for neighbor in neighbors[first] if mask & (1 << neighbor))
    return count((1 << len(ordered))-1)


def shuffle_skeleton(order: int, tiling: Tiling):
    """Delete colliding pairs, translate survivors, identify disjoint 2x2 holes.

    The intermediate survivor state is a partial tiling, not a full tiling.
    Coloring is recomputed using the *old* order before the size increases.
    """
    validate_tiling(order, tiling)
    translated = []
    for domino in tiling:
        (i, j), (k, ell) = sorted(domino)
        positive = (i+j+order) % 2 == 0
        dx, dy = ((0, 1 if positive else -1) if j == ell
                  else (1 if positive else -1, 0))
        translated.append(tuple((x+dx, y+dy) for x, y in domino))
    # A bad pair exchanges its two occupied domino spaces in one translation;
    # testing overlap *after* translation misses precisely these pairs.
    original_index = {frozenset(domino): index for index, domino in enumerate(tiling)}
    destroyed = set()
    for index, domino in enumerate(translated):
        partner = original_index.get(frozenset(domino))
        if partner is not None and frozenset(translated[partner]) == frozenset(tiling[index]):
            destroyed.update((index, partner))
    survivors = [domino for index, domino in enumerate(translated) if index not in destroyed]
    occupied = [cell for domino in survivors for cell in domino]
    target = cells(order+1)
    if len(occupied) != len(set(occupied)) or not set(occupied) <= target:
        raise ValueError("invalid translated survivor state")
    remaining = set(target) - set(occupied)
    holes = []
    while remaining:
        i, j = min(remaining)
        block = {(i, j), (i+1, j), (i, j+1), (i+1, j+1)}
        if not block <= remaining:
            raise ValueError("uncovered region is not a union of 2x2 holes")
        holes.append((i, j))
        remaining -= block
    return canonical(survivors), tuple(holes), len(destroyed)


def fill_holes(survivors, holes, choices) -> Tiling:
    choices = tuple(choices)
    if len(choices) != len(holes) or any(choice not in (0, 1) for choice in choices):
        raise ValueError("one binary choice is required per hole")
    dominoes = list(survivors)
    for (i, j), choice in zip(holes, choices):
        if choice == 0:
            dominoes += [((i, j), (i+1, j)), ((i, j+1), (i+1, j+1))]
        else:
            dominoes += [((i, j), (i, j+1)), ((i+1, j), (i+1, j+1))]
    return canonical(dominoes)


def shuffle_outcomes(order: int, tiling: Tiling):
    survivors, holes, _ = shuffle_skeleton(order, tiling)
    probability = Fraction(1, 2**len(holes))
    for choices in product((0, 1), repeat=len(holes)):
        yield fill_holes(survivors, holes, choices), probability


def sample(order: int, seed: int) -> Tiling:
    cells(order)
    random = Random(seed)
    tiling = ()
    for old_order in range(order):
        survivors, holes, _ = shuffle_skeleton(old_order, tiling)
        tiling = fill_holes(survivors, holes, (random.randrange(2) for _ in holes))
        validate_tiling(old_order+1, tiling)
    return tiling
