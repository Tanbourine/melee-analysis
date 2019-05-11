#!/usr/bin/env python
# encoding: utf-8
# Author: Darren Tan


import glob
import os
from slippi import Game
from slippi.id import ActionState, CSSCharacter, Stage
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime


class Distill():
    def __init__(self, file):
        self.game = Game(file)

        self._num_players = 4

        # game data
        self.duration = self.game.metadata.duration
        self.players = self.game.start.players
        self.tags = self._get_tags()

        # frame data
        self.data = self._parse_frames()
        self.rebirths = self._find_rebirths()
        self.death_percent = self._find_death_percent()

        # distill to json
        self._package_json()
        self._write_json()

    def _parse_frames(self):
        data = [[] for i in range(self._num_players)]
        for port in range(self._num_players):
            if self.players[port]:
                for frame in self.game.frames:
                    data[port].append(frame.ports[port].leader.post)
        return data

    def _get_tags(self):
        tags = []
        for i in range(self._num_players):
            if self.players[i]:
                tags.append(self.players[i].tag)
        return tags

    def _find_rebirths(self):
        rebirths = [[] for i in range(self._num_players)]
        for i, port in enumerate(self.data):
            if self.players[i]:
                j = 0
                while j < self.duration:
                    if port[j].state == ActionState.REBIRTH:
                        rebirths[i].append(j)
                        j += 60
                    else:
                        j += 1

        return rebirths

    def _find_death_percent(self):
        deaths = [[] for i in range(self._num_players)]
        for i, player in enumerate(self.data):
            if self.players[i]:
                for r_frame in self.rebirths[i]:
                    d_frame = r_frame - 1
                    deaths[i].append((d_frame, player[d_frame].damage))
        return deaths

    def _package_json(self):
        # packaging to distill to json
        self.dict = {
            'date': self.game.metadata.date.strftime('%Y%m%d_%H%M%S'),
            'stage': self.game.start.stage,
            'stocks': self.game.start.players[0].stocks,
        }

        for i in range(self._num_players):
            if self.players[i]:
                self.dict[i] = {
                    'char': self.game.start.players[i].character,
                    'tag': self.tags,
                    'deaths': self.death_percent[i],
                }

    def _write_json(self):
        # date = self.dict['date'].strftime('%Y%m%d_%H%M%S')
        filename = '../distilled/{}_{}_{}.json'.format(
            self.dict['date'], *self.tags)
        os.makedirs('../distilled/', exist_ok=True)
        with open(filename, 'w') as outfile:
            json.dump(self.dict, outfile, default=str, indent=4)

    def slice_state(self, port, start, end):
        data = []
        for i in range(start, end):
            frame = self.data[port][i]
            data.append((i, frame.damage, frame.stocks, frame.state))
        return data

    def plot_damage(self):
        fig, ax = plt.subplots(1, 1)

        p0_damage = []
        p1_damage = []
        for i in range(self.duration):
            p0_damage.append(self.data[0][i].damage)
            p1_damage.append(self.data[2][i].damage)

        ax.plot(p0_damage, label='Player 1')
        ax.plot(p1_damage, label='Player 2')

        for i, player in enumerate(self.death_percent):
            for death in player:
                ax.scatter(death[0], death[1])

        ax.legend(loc='best')
        plt.show()


def main():
    # file = '../replays/newgame.slp'
    # game = Distill(file)

    files = glob.glob('../replays/*.slp')
    print(files)
    for file in files:
        game = Distill(file)
        print("Done! {}".format(file))
        # game.plot_damage()

    # print(game._find_rebirths())
    # print(game._find_death_percent())

    # slice = game.slice_state(0, 4250, 4350)
    # print(slice)
    # print(game.players)


if __name__ == '__main__':
    main()
