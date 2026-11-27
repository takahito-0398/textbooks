"""Independent arithmetic checks of the book's sign and integer examples."""
from cmath import exp, phase
from fractions import Fraction
from math import gcd, pi


def winding(loop):
    points = [loop(exp(2j * pi * n / 512)) for n in range(513)]
    increments = [phase(right / left) for left, right in zip(points, points[1:])]
    return round(sum(increments) / (2 * pi))


def finite_quotient_invariants(first, second):
    """The invariant factors of Z² modulo the two independent columns."""
    entries_gcd = gcd(*first, *second)
    determinant = abs(first[0] * second[1] - first[1] * second[0])
    return entries_gcd, determinant // entries_gcd


def multiply_degree_one(left, right):
    """Multiply in Q[h]/(h²), with coefficients in increasing degree."""
    return left[0] * right[0], left[0] * right[1] + left[1] * right[0]


for m in (-4, -1, 0, 1, 3):
    assert winding(lambda z: z ** m) == m
    assert winding(lambda w: w.conjugate() ** m) == -m
assert winding(lambda z: z) == 1
assert winding(lambda z: z.conjugate()) == -1
print("S^2: w(z)=1; south positive-boundary winding=-1; Koszul clutching w(conj(z))=-1.")

# The equator diagrams vary the base point but keep the northern value fixed.
equator = (1, 1j, -1, -1j)
north_value = 1
assert tuple(z * north_value for z in equator) == equator
assert tuple(north_value for _ in equator) == (1, 1, 1, 1)
for z in equator:
    x, y = z.real, z.imag
    assert x*x+y*y == 1
    south_chart = complex(x, -y)
    assert south_chart == 1/z
    assert south_chart.conjugate() == z
assert winding(lambda z: z * z**-2) - winding(lambda z: z**-2) == 1
print("Equator figures: four coordinate pairs, south chart orientation, and the difference of winding numbers.")

assert finite_quotient_invariants((2, -3), (0, 2)) == (1, 4)
assert finite_quotient_invariants((2, 1), (0, 2)) == (1, 4)
assert finite_quotient_invariants((3, 3), (0, 3)) == (3, 3)
assert finite_quotient_invariants((4, 6), (0, 4)) == (2, 8)
print("Circle bundles: q=2 -> Z/4; q=3 -> Z/3 + Z/3; q=4 -> Z/2 + Z/8.")

for k in range(-12, 13):
    north = {n for n in range(-32, 33) if n >= 0}
    south = {n for n in range(-32, 33) if n <= k}
    kernel = len(north & south)
    excess = len(set(range(-32, 33)) - north - south)
    tangent_todd = (1, Fraction(2, 2))
    _, top_term = multiply_degree_one((1, k), tangent_todd)
    assert kernel - excess == top_term
    if k in (-2, 0):
        print(f"CP^1 O({k}): kernel={kernel}, cokernel={excess}, Todd integral={top_term}.")
