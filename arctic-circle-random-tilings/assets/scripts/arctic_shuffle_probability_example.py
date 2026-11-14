"""Exactly enumerate the order-2 to order-3 shuffling example in chapter 3."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from arctic_model import enumerate_tilings, shuffle_outcomes, shuffle_skeleton


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--order', type=int, choices=range(4), default=2)
    args = parser.parse_args()
    inputs = enumerate_tilings(args.order)
    paths = defaultdict(list)
    for source in inputs:
        _, holes, deleted_tiles = shuffle_skeleton(args.order, source)
        if deleted_tiles % 2:
            raise ValueError('a deleted pair must contain two dominoes')
        for output in shuffle_outcomes(args.order, source):
            paths[output].append((deleted_tiles // 2, len(holes)))
    summary = Counter()
    for histories in paths.values():
        kinds = set(histories)
        if len(kinds) != 1:
            raise ValueError('the finite example has inconsistent path counts')
        b, g = next(iter(kinds))
        probability = sum((Fraction(1, len(inputs) * 2**holes) for _, holes in histories), Fraction())
        summary[(b, g, len(histories), probability)] += 1
    for (b, g, preimages, probability), count in sorted(summary.items()):
        print(f'outputs={count}, b={b}, g={g}, preimages={preimages}, probability={probability}')
    print(f'order={args.order}, total outputs={len(paths)}')


if __name__ == '__main__':
    main()
