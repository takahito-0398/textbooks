"""Count points modulo primes and reproduce the historical BSD product.

Only the Python standard library is required.  The product omits bad primes;
this changes the multiplicative constant, not the predicted log-log slope.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Curve:
    name: str
    a: int
    b: int

    @property
    def discriminant(self) -> int:
        return -16 * (4 * self.a**3 + 27 * self.b**2)


CURVES = (
    Curve("rank0_y2=x3-x", -1, 0),
    Curve("rank1_y2=x3-2", 0, -2),
)


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0:1] = b"\x00"
    if limit >= 1:
        sieve[1:2] = b"\x00"
    for candidate in range(2, math.isqrt(limit) + 1):
        if sieve[candidate]:
            start = candidate * candidate
            count = (limit - start) // candidate + 1
            sieve[start : limit + 1 : candidate] = b"\x00" * count
    return [n for n in range(2, limit + 1) if sieve[n]]


def count_points(curve: Curve, prime: int) -> int:
    """Return #E(F_p), including the point at infinity."""
    square_counts = [0] * prime
    for y in range(prime):
        square_counts[(y * y) % prime] += 1

    affine = 0
    for x in range(prime):
        rhs = (x**3 + curve.a * x + curve.b) % prime
        affine += square_counts[rhs]
    return affine + 1


def experiment(limit: int) -> list[dict[str, int | float | str]]:
    rows: list[dict[str, int | float | str]] = []
    log_products = {curve.name: 0.0 for curve in CURVES}
    for prime in primes_up_to(limit):
        for curve in CURVES:
            if curve.discriminant % prime == 0:
                continue
            points = count_points(curve, prime)
            ap = prime + 1 - points
            log_products[curve.name] += math.log(points / prime)
            rows.append(
                {
                    "curve": curve.name,
                    "p": prime,
                    "N_p": points,
                    "a_p": ap,
                    "hasse_bound": 2 * math.sqrt(prime),
                    "log_log_p": math.log(math.log(prime)),
                    "log_partial_product": log_products[curve.name],
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=2000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = experiment(args.limit)
    fieldnames = list(rows[0])
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        writer = csv.DictWriter(__import__("sys").stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
