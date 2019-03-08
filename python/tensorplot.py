#!/usr/bin/env python
import os
import click
import tensorflow as tf
import json
import itertools


import numpy as np
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import yaml

def get_log_file(folder):
    return glob.glob(os.path.join(folder, '*events*'))[0]


def change_fontsize(ax, fs):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(fs)




# TODO use sns plot


@click.command()
@click.argument("config")
def main(config):
    '''
    colormap overview
    https://matplotlib.org/examples/color/colormaps_reference.html
    Parameters
    ----------
    config

    Returns
    -------

    '''
    with open(config) as handle:
        _dict = yaml.load(handle.read())

    log_files = _dict['logfiles']
    tags = _dict['tags']
    lw = _dict['lw']
    cmap = _dict['cmap']
    # Loading too much data is slow...
    tf_size_guidance = {
        'compressedHistograms': 10,
        'images': 0,
        'scalars': 100,
        'histograms': 1
    }

    LINESTYLES = ['-', '--', '-.', ':']
    np.random.seed(42)
    COLORS = plt.get_cmap(cmap)(np.random.random(10), bytes=False)[:, :3]  # TODO better colors

    data = {}

    for key, log_folder in log_files.items():
        log_file = get_log_file(log_folder)
        event_acc = EventAccumulator(log_file, tf_size_guidance)
        event_acc.Reload()
        this_data = {}
        g = event_acc.Scalars('global_step_1')
        g = list(map(lambda x: x.value, g))
        this_data['global_step'] = g
        for e in tf.train.summary_iterator(log_file):
            for v in e.summary.value:
                if v.tag in tags:
                    values = event_acc.Scalars(v.tag)
                    values = list(map(lambda x: x.value, values))
                    this_data[v.tag] = values
        data[key] = this_data


    with plt.style.context('seaborn-bright'):
        for t in tags: # create plot for every tag
            linestyles = itertools.cycle(LINESTYLES)
            colors = itertools.cycle(COLORS)
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            for label, this_data in data.items():
                ax.plot(this_data['global_step'], this_data[t], label=label, linewidth=lw,
                        linestyle=next(linestyles),
                        color=next(colors))
            ax.set_xlabel('step')
            ax.set_ylabel(str(t))
            ax.legend(fontsize=24,
                      frameon=True)
            ax.grid(True)
            change_fontsize(ax, 20)
            fig.tight_layout()
            fname = '{}.png'.format(t)
            plt.savefig(fname)


    # plt.xlabel("Steps")
    # plt.ylabel("Accuracy")
    # plt.title("Training Progress")
    # plt.legend(loc='upper right', frameon=True)
    # plt.show()


if __name__ == '__main__':
    main()