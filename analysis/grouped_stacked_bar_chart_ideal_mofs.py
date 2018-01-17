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



# by row: U + K, pair, bond, angle
rows = np.array([[-4.78E-10, -4.78E-10, -6.34E-10, -6.34E-10, 1.71E-08, 1.71E-08],
        [0.00E+00, 0.00E+00, 0.00E+00, 0.00E+00, 0.00E+00, 0.00E+00],
        [-9.53E-07, -9.53E-07, -4.36E-06, -4.36E-06, -4.40E-06, -4.40E-06],
        [-1.06E-09, -1.41E-07, -1.01E-08, -7.04E-07, 2.87E-09, -7.12E-07]
        ]) * -1
y_range = [0, 5.5e-6]
y_ticklabels = [0, 1e-6, 2e-6, 3e-6, 4e-6]

# temporary correction to normalize data; need to correct in data set
rows[3][0] = rows[3][0] * 5.13 / 1.11
rows[3][1] = rows[3][1] * 5.13 / 1.11
rows[2][0] = rows[2][0] * 5.13 / 1.11
rows[2][1] = rows[2][1] * 5.13 / 1.11

# x_labels = [ "%s-%s" % (human_format(row - avg_every * timesteps_per_row), human_format(row)) for row in rows]



colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fdbf6f','#ffff99','#ff7f00','#cab2d6','#6a3d9a','#b15928','#fb9a99','#e31a1c']

num_plots = 1
bar_width = 0.65
bar_buffer = bar_width / 2
bar_indices = np.arange(len(rows))
bar_x = np.array([1,2,4,5,7,8])



#### plot all plots
fig = plt.figure(figsize=(7,5))
fig.set_tight_layout(False)
fig.subplots_adjust(right=0.8)
ax = fig.add_subplot(1, 1, 1)

ax.set_ylim([0, 5.8e-6])

ax.set_title("Per-term original and corrected heat fluxes for idealized MOFS", weight="bold")
ax.set_xlabel("")
ax.set_ylabel("Heat Flux [$Kcal / (mol \cdot fs \cdot Å^2)$]")

ax.yaxis.grid(linestyle='-', color='0.7', zorder=0)
ax.set_xticks(bar_x)
ax.set_xticklabels(["orig","corr", "orig","corr", "orig","corr"])
ax.set_yticklabels(y_ticklabels)
# ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
labelsypos = -0.8e-6
ax.text((bar_x[0] + bar_x[1])/2, labelsypos, 'Cubic', horizontalalignment="center")
ax.text((bar_x[2] + bar_x[3])/2, labelsypos, 'Triangular', horizontalalignment="center")
ax.text((bar_x[4] + bar_x[5])/2, labelsypos, 'Hexagonal', horizontalalignment="center")

ax.axhline(5.13e-6, linestyle='dashed', linewidth=2, label="Expected")
ax.text(0.65/2 - 0.15, 5.13e-6, '5.13e-06', ha="right", va="center", weight="bold")




# ax.set_ylim(y_range)
# ax.set_xlim(x_range)

legend_labels = ["Expected", None, None, "Bond", "Angle"]
prior_vals = np.zeros(len(rows[0]))
for i, row in enumerate(rows):
    ax.bar(bar_x, row, bar_width, color=colors[i], bottom=prior_vals, zorder=3, label=legend_labels[i+1])
    prior_vals += row

ax.legend(bbox_to_anchor=(1, 1))
# ax.legend(["Expected", None, None, "bond", "angle"], bbox_to_anchor=(1, 1))


fig.savefig("orig_corr_hf_for_idealized_mofs.png", dpi=288)
