#!/usr/bin/env python
# encoding: utf-8
# Author: Darren Tan


from slippi import Game
import numpy as np
import matplotlib.pyplot as plt


class MeleeAnalysis():
    def __init__(self, file):
        self.game = Game(file)

        self.duration = self.game.metadata.duration
        self.ports = [self.parse_frames(0), self.parse_frames(1)]
        # self.port0 = self.parse_frames(0)
        # self.port1 = self.parse_frames(1)

    def parse_frames(self, port):
        data = []
        for frame in self.game.frames:
            data.append(frame.ports[port].leader.post)
        return data

    def plot_damage(self):
        fig, ax = plt.subplots(1, 1)

        p0_damage = []
        p1_damage = []
        for i in range(self.duration):
            p0_damage.append(self.ports[0][i].damage)
            p1_damage.append(self.ports[1][i].damage)

        ax.plot(p0_damage)
        ax.plot(p1_damage)
        plt.show()

    def slice_state(self, port, start, end):
        data = []
        for i in range(start, end):
            data.append(self.ports[port][i].state)
        return data


def main():
    file = 'replays/newgame.slp'
    game = MeleeAnalysis(file)

    game.plot_damage()

    # for i in range(1800, 1870):
    #     print(game.ports[1][i].state)

    # slice = game.slice_state(1, 1830, 1870)
    # print(slice)


if __name__ == '__main__':
    main()
