#!/usr/bin/env python
# encoding: utf-8
# Author: Darren Tan

import json
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


class Stats():
    def __init__(self):
        self.data = []
        files = glob.glob('../distilled/*.json')
        for file in files:
            with open(file, 'r') as f:
                self.data.append(json.load(f))

        self.dates = self.get_date()

    def avg_death_perc(self, port):
        assert isinstance(port, str), "Port input must be type(str)"
        percents = []
        for game in self.data:
            # print(game)
            deaths = game[port]['deaths']
            game_percents = []
            for death in game[port]['deaths']:
                game_percents.append(death[1])

            game_percents = np.array(game_percents)
            percents.append(game_percents.mean())

        return np.array(percents)

    def get_date(self):
        dates = []
        for game in self.data:
            dates.append(datetime.strptime(
                game['date'], '%Y%m%d_%H%M%S'))
        return dates

    def plot_avg_death_perc(self, port):
        fig, ax = plt.subplots(1, 1)

        print(self.dates, self.avg_death_perc(port))
        ax.scatter(self.dates, self.avg_death_perc(
            port), label='Port {}'.format(port))

        # auto space x ticks on graph
        index = np.round(np.linspace(
            0, len(self.dates) - 1, 10)).astype(int)
        xticks = []
        for idx in index:
            xticks.append(self.dates[idx])
        ax.set_xticks(xticks)

        # plot settings
        ax.set_title('AVERAGE DEATH PERCENT', fontsize=8)
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S'))
        ax.set_ylabel('Damage [%]', fontsize=9)
        ax.tick_params(axis='both', labelsize=6)
        ax.legend(loc='best', fontsize=6)
        fig.tight_layout()
        fig.autofmt_xdate(rotation=60)
        plt.grid()
        plt.show()


def main():
    stats = Stats()
    stats.plot_avg_death_perc('0')


if __name__ == '__main__':
    main()
