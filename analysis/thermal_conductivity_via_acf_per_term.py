
from glob import glob
from os.path import basename, join


import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from scipy.integrate import cumtrapz, simps

from analysis.utils import save_figure_as_tiff

def average_acfs(acfpath, acf_size):
    total_acf = np.zeros((acf_size))

    acf_files = glob(acfpath)
    print(acfpath, acf_files)
    print('len: ', len(acf_files))
    for acf_file in acf_files:
        total_acf += np.loadtxt(acf_file)[:,3]
        print('*')

    return total_acf / len(acf_files)

base_dir = "/Users/pboone/Dropbox (Personal)/Projects/LAMMPS Heat Flux Fix/LAMMPS run files/h1-hydrocarbons/c8h18-octane-emd-gk-72C-40A-breakdown-2/acf_outputs"

acf_labels = ["T2", "T3", "T4", "T3i", "T4i"]
acf_globs = ["*J0Jt2_*.dat", "*J0Jt3_*.dat", "*J0Jt4_*.dat", "*J0Jt3i_*.dat", "*J0Jt4i_*.dat"]
acfs = [average_acfs(join(base_dir, acf_label), 100000) for acf_label in acf_globs]

## 40 angstrom box 5t
volume = 40.00 ** 3
temp = 345.28 # K
nemd_k = 167.0
experimental_k = 187.40

boltzmann_const = 1.3806504e-23 # J / K
kcal2j = 4186.0/6.02214e23  # kCal / mol to Joules
ang2m = 1.0e-10             # Angstroms to meters
fs2s = 1.0e-15              # Femtoseconds to seconds
convert = kcal2j**2 / (fs2s * ang2m) # kCal^2 / angstroms femtosecond => J / m s
sample_fs = 5
prefactor =  volume * convert * sample_fs / (boltzmann_const * temp**2)


all_indices = np.arange(0, 100000) / 1000 # convert to [ps]

plot_points = [1400, acfs[0].shape[0]] # 7ps, all data


##### print thermal conductivity plot (two ranges)
plot_labels = ("(A)", "(B)")
plot_label_pos = (0.10, 0.60)

rcParams.update({'figure.autolayout': True})

fs = 7
fsl = fs
fig = plt.figure(figsize=(7,3), dpi=300, tight_layout=True)

for plot_index in range(len(plot_points)):
    pp = plot_points[plot_index]
    indices = all_indices[:pp] * sample_fs

    ax = fig.add_subplot(1, 2, plot_index + 1)

    ax.set_title(plot_labels[plot_index])
    ax.tick_params(axis='x', which='major', labelsize=fs)
    ax.tick_params(axis='y', which='major', labelsize=fs)
    ax.set_xlabel('($\\tau$ [ps]', fontsize=fsl)

    ax.set_ylabel('$\kappa$ [W / m K]', fontsize=fsl)
    # ax.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax.grid(linestyle='-', color='0.7', zorder=0)

    for i, acf_label in enumerate(acf_labels):
        int_one_traj = prefactor * cumtrapz(acfs[i][:pp])
        ax.plot(indices[:-1], int_one_traj, zorder=0, lw=0.5, label=acf_label)

    ax.axhline(experimental_k / 1000, linestyle='dashed', linewidth=1, label="Experimental", color="black")
    ax.axhline(nemd_k / 1000, linestyle='dashed', linewidth=1, label="NEMD", color="0.4")
    ax.legend(fontsize=fsl)

save_figure_as_tiff(fig, "figures/acf_thermal_conductivity_two_ranges_per_term.tif", dpi=300)
