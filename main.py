#!/usr/bin/env python
# encoding: utf-8
# Author: Darren Tan

import glob
from melee_analysis import Distill, Stats


def distill():
    files = glob.glob('replays/*.slp')
    print("{} replay files detected: {}".format(len(files), files))
    for file in files:
        game = Distill(file, 'distilled/')
        print("Done! {}".format(file))
        # game.plot_damage()


def stats():
    stats = Stats('distilled/')
    stats.plot_avg_death_perc('0')


def main():
    distill()
    # stats()


if __name__ == '__main__':
    main()
