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


# by row: U + K, pair, bond, angle, dihedral, improper
rows = np.array([[0.008430, 0.008430, 0.007510, 0.007510],
                 [0.048900, 0.048900, 0.047300, 0.047300],
                 [0.010200, 0.010200, 0.012200, 0.012200],
                 [0.004070, 0.010700, 0.005100, 0.008970],
                 [0.000252, 0.007150, 0.000000, 0.000000],
                 [0.000000, 0.000000, 0.001320, 0.009750]])



expected_hf = np.array([0.086276, 0.086276, 0.086276, 0.086276])

# now in fraction total expected
rows = rows / expected_hf

y_range = [0, 1.1]
# y_ticklabels = np.arange(0,11)/10



colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fdbf6f','#cab2d6','#6a3d9a','#b15928','#fb9a99','#e31a1c']

num_plots = 1
bar_width = 0.65
bar_buffer = bar_width / 2
bar_indices = np.arange(len(rows))
bar_x = np.array([1,2,3.5,4.5])



#### plot all plots
fs = 7
fsl = fs
fig = plt.figure(figsize=(3.5,3), tight_layout=True)
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim((0,5.5))
ax.tick_params(axis='x', which='major', labelsize=fs)
ax.tick_params(axis='y', which='major', labelsize=fs)


# ax.set_title("Per-term original and corrected heat fluxes for hydrocarbons", weight="bold")
ax.set_xlabel("")
ax.set_ylabel("Fraction of applied heat flux", fontsize=fsl)

ax.yaxis.grid(linestyle='-', color='0.7', zorder=0)
ax.set_xticks(bar_x)
ax.set_xticklabels(["LAMMPS", "w/ fix", "LAMMPS", "w/ fix"])
# ax.set_yticklabels(y_ticklabels)
# ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
labelsypos = -0.14
ax.text((bar_x[0] + bar_x[1])/2, labelsypos, 'Dihedral', horizontalalignment="center", fontsize=fsl)
ax.text((bar_x[2] + bar_x[3])/2, labelsypos, 'Improper', horizontalalignment="center", fontsize=fsl)
# ax.text((bar_x[7] + bar_x[9])/2, labelsypos, 'Hexadecane C16H34', horizontalalignment="center")
# ax.text((bar_x[4] + bar_x[5])/2, labelsypos, 'Hexagonal', horizontalalignment="center")

ax.axhline(1.0, linestyle='dashed', linewidth=1, label="Expected", color="black")
# ax.text(0.65/2 - 0.15, 1.0, '1.0', ha="right", va="center", weight="bold")

ax.set_ylim(y_range)
# ax.set_xlim(x_range)

legend_labels = ["Expected", "Convection", "Pair", "Bond", "Angle", "Dihedral", "Improper"]
prior_vals = np.zeros(len(rows[0]))
for i, row in enumerate(rows):
    ax.bar(bar_x, row, bar_width, color=colors[i], bottom=prior_vals, zorder=3, label=legend_labels[i+1])
    prior_vals += row

ax.legend(loc=(0.05, 0.14), framealpha=1.0, fontsize=fsl)
# ax.legend(["Expected", None, None, "bond", "angle"], bbox_to_anchor=(1, 1))


fig.savefig("orig_corr_hf_for_impropers.png", dpi=600)
