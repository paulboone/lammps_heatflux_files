#!/usr/bin/env python3

import argparse
import csv
from math import ceil
import sys

from matplotlib import pyplot as plt
from matplotlib import rcParams
import numpy as np

from lammps_tools.utils import human_format

rcParams.update({'figure.autolayout': True})

# by row: U + K, pair, bond, angle, dihedral = 0, improper = 0
rows = np.array([[45.46, 76.45, 70.15, 73.02, 70.64, 57.51],
                 [253.51, 185.87, 148.49, 134.82, 111.89, 95.89],
                 [0.00, 24.23, 27.57, 36.33, 39.94, 72.21],
                 [0.00, 6.20, 26.25, 25.43, 45.23, 41.03],
                 [0.00, 9.58, 28.13, 31.04, 32.44, 33.15]])


expected_hf = np.array([300]*6)

# now in fraction total expected
rows = rows / expected_hf

y_range = [0, 1.1]
# y_ticklabels = np.arange(0,11)/10



colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fdbf6f','#ffff99','#ff7f00','#cab2d6','#6a3d9a','#b15928','#fb9a99','#e31a1c']

num_plots = 1
bar_width = 0.65
bar_buffer = bar_width / 2
bar_indices = np.arange(len(rows))
bar_x = np.array([1,2,3,4,5,6])



#### plot all plots
fig = plt.figure(figsize=(7,5))
fig.set_tight_layout(False)
fig.subplots_adjust(right=0.8)
ax = fig.add_subplot(1, 1, 1)

# ax.set_title("Per-term original and corrected heat fluxes for hydrocarbons", weight="bold")
ax.set_xlabel("")
ax.set_ylabel("Fraction of expected Heat Flux")

ax.yaxis.grid(linestyle='-', color='0.7', zorder=0)
ax.set_xticks(bar_x)
ax.set_xticklabels(["CH4", "C4H10", "C8H18", "C10H22", "C16H34", "C24H50",])

ax.axhline(1.0, linestyle='dashed', linewidth=1, label="Expected", color="black", zorder=2)
# ax.text(0.65/2 - 0.15, 1.0, '1.0', ha="right", va="center", weight="bold")

ax.set_ylim(y_range)
# ax.set_xlim(x_range)

legend_labels = ["Expected", "KE + PE", "Pair", "Bond", "Angle", "Dihedral"]
prior_vals = np.zeros(len(rows[0]))
for i, row in enumerate(rows):
    ax.bar(bar_x, row, bar_width, color=colors[i], bottom=prior_vals, zorder=3, label=legend_labels[i+1])
    prior_vals += row

ax.legend(bbox_to_anchor=(1, 1))
# ax.legend(["Expected", None, None, "bond", "angle"], bbox_to_anchor=(1, 1))


fig.savefig("ohara_hydrocarbons.png", dpi=288)
