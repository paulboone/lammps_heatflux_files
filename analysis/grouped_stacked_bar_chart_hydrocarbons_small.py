#!/usr/bin/env python3

import argparse
import csv
from math import ceil
import sys

from matplotlib import pyplot as plt
from matplotlib import rcParams
import numpy as np

from analysis.utils import save_figure_as_tiff
from lammps_tools.utils import human_format

rcParams.update({'figure.autolayout': True})


# by row: U + K, pair, bond, angle, dihedral, improper
rows = np.array([[0.00769, 0.00769, 0.008430, 0.008430, 0.020100, 0.020100],
                 [0.05700, 0.05700, 0.048900, 0.048900, 0.035500, 0.035500],
                 [0.00378, 0.00378, 0.010200, 0.010200, 0.016300, 0.016300],
                 [0.00215, 0.00361, 0.004070, 0.010700, 0.002080, 0.012500],
                 [0.00000, 0.00000, 0.000252, 0.007150,-0.000566, 0.009830],
                 [0.00000, 0.00000, 0.000000, 0.000000, 0.000000, 0.000000]])

expected_hf = np.array([0.072823, 0.072823, 0.086276, 0.086276, 0.094666, 0.094666])

# now in fraction total expected
rows = rows / expected_hf

y_range = [0, 1.1]
# y_ticklabels = np.arange(0,11)/10



colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fdbf6f','#ffff99','#ff7f00','#cab2d6','#6a3d9a','#b15928','#fb9a99','#e31a1c']

num_plots = 1
bar_width = 0.65
bar_buffer = bar_width / 2
bar_indices = np.arange(len(rows))
bar_x = np.array([1,2,3.5,4.5,6,7])



#### plot all plots
fig = plt.figure(figsize=(4.5,3))
fig.set_tight_layout(False)
fig.subplots_adjust(right=0.7, bottom=0.2)
ax = fig.add_subplot(1, 1, 1)

# ax.set_title("Per-term original and corrected heat fluxes for hydrocarbons", weight="bold")
ax.set_xlabel("")
ax.set_ylabel("Fraction of expected heat flux")

ax.yaxis.grid(linestyle='-', color='0.7', zorder=0)
ax.set_xticks(bar_x)
ax.set_xticklabels(["orig","corr", "orig","corr", "orig","corr"])
# ax.set_yticklabels(y_ticklabels)
# ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
labelsypos = -0.20
ax.text((bar_x[0] + bar_x[1])/2, labelsypos, 'C3H8', horizontalalignment="center")
ax.text((bar_x[2] + bar_x[3])/2, labelsypos, 'C8H18', horizontalalignment="center")
ax.text((bar_x[4] + bar_x[5])/2, labelsypos, 'C16H34', horizontalalignment="center")
# ax.text((bar_x[4] + bar_x[5])/2, labelsypos, 'Hexagonal', horizontalalignment="center")

ax.axhline(1.0, linestyle='dashed', linewidth=1, label="Expected", color="black")
# ax.text(0.65/2 - 0.15, 1.0, '1.0', ha="right", va="center", weight="bold")

ax.set_ylim(y_range)
# ax.set_xlim(x_range)

legend_labels = ["Expected", "Convection", "Pair", "Bond", "Angle", "Dihedral", ""]
prior_vals = np.zeros(len(rows[0]))
for i, row in enumerate(rows):
    ax.bar(bar_x, row, bar_width, color=colors[i], bottom=prior_vals, zorder=3, label=legend_labels[i+1])
    prior_vals += row

ax.legend(bbox_to_anchor=(1, 1))
# ax.legend(["Expected", None, None, "bond", "angle"], bbox_to_anchor=(1, 1))

save_figure_as_tiff(fig, "figures/orig_corr_hf_for_hydrocarbons_small.tif", dpi=300)
