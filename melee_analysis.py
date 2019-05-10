#!/usr/bin/env python
# encoding: utf-8
# Author: Darren Tan


from slippi import Game
from slippi.id import ActionState
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

        ax.plot(p0_damage, label='Player 1')
        ax.plot(p1_damage, label='Player 2')
        ax.legend(loc='best')
        plt.show()

    def slice_state(self, port, start, end):
        data = []
        for i in range(start, end):
            frame = self.ports[port][i]
            data.append((i, frame.damage, frame.stocks, frame.state))
        return data

    def find_rebirths(self):
        rebirths = []
        for i, port in enumerate(self.ports):
            for j, frame in enumerate(port):
                # if frame.state == ActionState.REBIRTH:
                if frame.state == ActionState.REBIRTH:
                    rebirths.append((i, j))

        # filter out frames from the same rebirth
        slim_rebirths = []
        for n in range(0, len(rebirths), 60):
            slim_rebirths.append(rebirths[n])

        return slim_rebirths




def main():
    file = 'replays/newgame.slp'
    game = MeleeAnalysis(file)


    rebirths = game.find_rebirths()
    print(rebirths)

    # slice = game.slice_state(0, 4250, 4350)
    # print(slice)

    # game.plot_damage()

if __name__ == '__main__':
    main()
