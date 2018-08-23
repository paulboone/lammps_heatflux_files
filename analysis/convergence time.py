import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.utils import save_figure_as_tiff

rows_to_avg = 100
expected_heat_flux = -0.086276

# hf = np.loadtxt(sys.stdin)
# rows, (timestep, original, corrected)
hf = np.loadtxt("hf.txt", skiprows=1)
df = pd.DataFrame(hf)
df1 = df.groupby(lambda x: x // rows_to_avg).mean()
t = (df1[0] - 2000000) / 1000000
lammps_data = df1[[1,2]] / expected_heat_flux

# t[-100:]

# last_cut = 100
# t = t[-last_cut:]
# lammps_data = lammps_data[-last_cut:]

stddev = np.std(lammps_data)
print(stddev)
print(stddev[1] - stddev[2])


fs = 7
fsl = fs
fig = plt.figure(figsize=(3.5,3))
ax = fig.add_subplot(1, 1, 1)
ax.tick_params(axis='x', which='major', labelsize=fs)
ax.tick_params(axis='y', which='major', labelsize=fs)

ax.axhline(1.0, linestyle='dashed', linewidth=1, label="Expected", color="black", zorder=2)
ax.plot(t, lammps_data, zorder=2)
ax.set_xlabel('Timesteps', fontsize=fsl)
ax.set_xticks([0, 3, 10, 20, 30, 40])
ax.set_xticklabels(["0", "3M", "10M", "20M", "30M", "40M"])
ax.set_ylabel("Fraction of applied heat flux", fontsize=fsl)
ax.grid(linestyle='-', color='0.7', zorder=0)
ax.axvspan(0,3, color="0.9", label='No applied heat flux')

legend_labels = ["Applied heat flux", "Uncorrected LAMMPS", "Corrected LAMMPS"]
legend = ax.legend(legend_labels, framealpha=1.0, fontsize=fsl)

save_figure_as_tiff(fig, "figures/total_heat_flux_convergence_100.tif", dpi=300)



# fig.savefig("total_heat_flux_convergence_100.png", dpi=300)
