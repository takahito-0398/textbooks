"""Finite Monte Carlo of the step process near sites 0 and 1.

The truncation starts at -steps: particles initially farther left cannot reach
site 0 within the simulated horizon. Updates use candidates from the old state.
"""
import argparse
import random


def simulate(trials, steps, seed):
    if trials < 1 or steps < 0:
        raise ValueError('trials must be positive and steps nonnegative')
    rng = random.Random(seed)
    occupancy = [0] * (steps + 1)
    movable = [0] * (steps + 1)
    crossings = [0] * steps
    for _ in range(trials):
        particles = set(range(-steps, 1))
        for time in range(steps + 1):
            occupancy[time] += 0 in particles
            movable[time] += 0 in particles and 1 not in particles
            if time == steps:
                break
            old_candidates = [site for site in particles if site + 1 not in particles]
            moves = [site for site in old_candidates if rng.randrange(2)]
            crossings[time] += 0 in moves
            particles.difference_update(moves)
            particles.update(site + 1 for site in moves)
    return occupancy, movable, crossings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trials', type=int, default=10000)
    parser.add_argument('--steps', type=int, default=4)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    occupancy, movable, crossings = simulate(args.trials, args.steps, args.seed)
    print(f'trials={args.trials}, steps={args.steps}, seed={args.seed}')
    print('time  P(X0=1)  P(10 at 0,1)  observed crossings in next update')
    for time in range(args.steps + 1):
        observed = f'{crossings[time] / args.trials:.4f}' if time < args.steps else '-'
        print(f'{time:>4}  {occupancy[time] / args.trials:.4f}     {movable[time] / args.trials:.4f}          {observed}')


if __name__ == '__main__':
    main()
