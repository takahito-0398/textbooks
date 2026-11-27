"""Check book references and exact arithmetic in selected worked examples."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial, gcd, prod
from pathlib import Path
import re


def check_sources():
    book = Path(__file__).resolve().parents[1]
    chapters = sorted((book / 'chapters').glob('*.qmd'))
    all_labels = {}
    counts = Counter()
    used_figures = set()
    for chapter in chapters:
        source = chapter.read_text(encoding='utf-8')
        sections = len(re.findall(r'^## ', source, re.M))
        assert source.count('**導入。**') == sections, chapter
        assert source.count('::: {.ku-summary}') == sections, chapter
        assert source.count('**章の導入**') == source.count('**章のまとめ**') == 1, chapter
        assert '::: {.ku-worked}' in source, chapter
        counts['sections'] += sections
        counts['worked'] += source.count('::: {.ku-worked}')
        labels = re.findall(r'\{#((?:eq|fig|tbl)-[\w-]+)(?:[ \t]+[^}\n]*)?\}', source)
        assert len(labels) == len(set(labels)), chapter
        for label in labels:
            assert label not in all_labels, label
            all_labels[label] = chapter
        assert not re.search(r'(?<=\S)@(?:eq|fig|tbl)-', source), chapter
        local_refs = re.findall(r'@((?:eq|fig|tbl)-[\w-]+)', source)
        assert set(local_refs) <= set(labels), (chapter, set(local_refs) - set(labels))
        counts.update(label.split('-', 1)[0] for label in labels)
        counts['references'] += len(local_refs)
        edges = re.findall(r'^ *\$\$', source, re.M)
        assert len(edges) % 2 == 0, chapter
        counts['displays'] += len(edges) // 2
        for relative in re.findall(r'!\[[^\]\n]*\]\(([^)\n]*assets/figures/[^)\s]+)', source):
            figure = (chapter.parent / relative).resolve()
            assert figure.is_file() and figure.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'), figure
            used_figures.add(figure)
    for chapter in chapters:
        source = chapter.read_text(encoding='utf-8')
        for target, label in re.findall(r'\(([^()\s]+\.qmd)#((?:eq|fig|tbl)-[\w-]+)\)', source):
            assert all_labels.get(label) == (chapter.parent / target).resolve(), (chapter, target, label)
            counts['cross_chapter_references'] += 1
    assert used_figures == {p.resolve() for p in (book / 'assets/figures').glob('*.png')}
    print(f'{len(chapters)} chapters, {len(used_figures)} original figure assets: {dict(counts)}')


def determinant(matrix):
    size = len(matrix)
    return sum(
        (-1) ** sum(p[i] > p[j] for i, j in combinations(range(size), 2))
        * prod(matrix[i][p[i]] for i in range(size))
        for p in permutations(range(size))
    )


def check_lens_spaces():
    examples = {
        (2, 2): (1, 4), (3, 2): (3, 3), (3, 3): (1, 3, 9),
        (4, 3): (2, 2, 16), (6, 3): (1, 3, 72),
    }
    for (power, dimension), smith in examples.items():
        relations = [[comb(power, i - j + 1) if i >= j else 0
                      for j in range(dimension)] for i in range(dimension)]
        divisors = [1]
        for k in range(1, dimension + 1):
            subsets = list(combinations(range(dimension), k))
            divisors.append(gcd(*(
                determinant([[relations[i][j] for j in cols] for i in rows])
                for rows in subsets for cols in subsets
            )))
        assert tuple(b // a for a, b in zip(divisors, divisors[1:])) == smith
        assert prod(smith) == power ** dimension


def multiply(left, right, degree):
    return [sum(left[i] * right[k-i] for i in range(k+1)) for k in range(degree+1)]


def check_projective_space():
    for n in range(1, 9):
        # The coefficients of (1-exp(-h))/h determine its reciprocal recursively.
        denominator = [Fraction((-1)**i, factorial(i+1)) for i in range(n+1)]
        todd = [Fraction(1)] + [Fraction(0)] * n
        for k in range(1, n+1):
            todd[k] = -sum(denominator[i] * todd[k-i] for i in range(1, k+1))
        power = [1] + [0] * n
        for _ in range(n+1):
            power = multiply(power, todd, n)
        for k in range(-n-4, n+5):
            exponential = [Fraction(k**i, factorial(i)) for i in range(n+1)]
            expected = Fraction(prod(k+i for i in range(1, n+1)), factorial(n))
            assert multiply(exponential, power, n)[n] == expected, (n, k)
        for i in range(n+1):
            for j in range(n+1):
                entry = sum(
                    (i+k <= n) * ((k+j == n) - (k+j == n+1))
                    for k in range(n+1)
                )
                assert entry == (i == j), (n, i, j)
    for s in range(2, 20):
        assert -sum(range(1, s)) == -((-s) * (1-s)) // 2


def check_torus_recurrence():
    # Compare exponents in C_(j+m) / C_j for either sign of the degree m.
    for m in (*range(-8, 0), *range(1, 9)):
        for j in range(-24, 25):
            exponent_difference = -Fraction((j+m)**2 - j**2, m)
            assert exponent_difference == -(2*j + m)


if __name__ == '__main__':
    check_sources()
    check_lens_spaces()
    check_projective_space()
    check_torus_recurrence()
    print('Exact checks passed: Smith minors, projective Todd integrals and diagonal, negative family index, torus recurrence')
