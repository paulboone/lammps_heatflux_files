#!/usr/bin/env python3

import argparse
import csv
from math import ceil
import sys

from matplotlib import pyplot as plt
from matplotlib import rcParams
import numpy as np

from utils import human_format

rcParams.update({'figure.autolayout': True})



# by row: U + K, pair, bond, angle, dihedral = 0, improper = 0

rows = np.array([[0.00041, 0.00041, 0.00021, 0.00021, 0.01710, 0.01710],
                 [0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
                 [0.82300, 0.82300, 1.45000, 1.45000, 4.39000, 4.39000],
                 [0.00091, 0.12200, 0.00335, 0.23400, 0.00286, 0.71000]])


expected_hf = np.array([0.96, 0.96, 1.70600, 1.70600, 5.118, 5.118])

# now in fraction total expected
rows = rows / expected_hf

y_range = [0, 1.1]
# x_labels = [ "%s %s" % (human_format(row   avg_every * timesteps_per_row), human_format(row)) for row in rows]



colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fdbf6f','#ffff99','#ff7f00','#cab2d6','#6a3d9a','#b15928','#fb9a99','#e31a1c']

num_plots = 1
bar_width = 2.5*0.65
bar_buffer = bar_width / 2
bar_indices = np.arange(len(rows))
bar_x = np.array([1,3,6,8,11,13])



#### plot all plots
fig = plt.figure(figsize=(7,5))
fig.set_tight_layout(False)
fig.subplots_adjust(right=0.8)
ax = fig.add_subplot(1, 1, 1)

ax.set_ylim(y_range)

ax.set_title("Per-term original and corrected heat fluxes for idealized MOFS", weight="bold")
ax.set_xlabel("")
ax.set_ylabel("Fraction of expected Heat Flux")

ax.yaxis.grid(linestyle='', color='0.7', zorder=0)
ax.set_xticks(bar_x)
ax.set_xticklabels(["original", "corrected", "original", "corrected", "original","corrected"])
# ax.set_yticklabels(y_ticklabels)
# ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
labelsypos = -0.15
ax.text((bar_x[0] + bar_x[1])/2, labelsypos, 'Cubic', horizontalalignment="center")
ax.text((bar_x[2] + bar_x[3])/2, labelsypos, 'Triangular', horizontalalignment="center")
ax.text((bar_x[4] + bar_x[5])/2, labelsypos, 'Hexagonal', horizontalalignment="center")

ax.axhline(1.0, linestyle='dashed', linewidth=1, label="Expected", color="black")
# ax.text(0.65/2,  0.15, 5.13e6, '5.13e06', ha="right", va="center", weight="bold")

# ax.set_xlim(x_range)

# legend_labels = ["Expected", "KE", "Pair", "Bond", "Angle"]
legend_labels = ["Expected", None, None, "Bond", "Angle"]
prior_vals = np.zeros(len(rows[0]))
for i, row in enumerate(rows):
    ax.bar(bar_x, row, bar_width, color=colors[i], bottom=prior_vals, zorder=3, label=legend_labels[i+1])
    prior_vals += row

ax.legend(bbox_to_anchor=(1, 1))
# ax.legend(["Expected", None, None, "bond", "angle"], bbox_to_anchor=(1, 1))


fig.savefig("orig_corr_hf_for_idealized_mofs.png", dpi=288)
