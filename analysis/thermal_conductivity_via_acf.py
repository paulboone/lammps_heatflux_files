
from glob import glob
from os.path import basename

import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from scipy.integrate import cumtrapz, simps

from analysis.utils import save_figure_as_tiff

def all_acfs(acfpath, acf_size):

    acf_files = list(glob(acfpath))
    acf_files.sort()
    if len(acf_files) % 3 != 0:
        raise Exception("ERROR: # of acf files should be a multiple of 3")

    print('len: ', len(acf_files))
    acfs = np.zeros((len(acf_files) // 3, acf_size))
    one_traj_acfs = np.zeros((3,acf_size))
    for i in range(0,len(acf_files) // 3):

        one_traj_acfs[0] = np.loadtxt(acf_files[i*3])[:,3]
        one_traj_acfs[1] = np.loadtxt(acf_files[i*3 + 1])[:,3]
        one_traj_acfs[2] = np.loadtxt(acf_files[i*3 + 2])[:,3]
        acfs[i] = np.average(one_traj_acfs, axis=0)
        print("averaging: %s, %s, %s" % (   basename(acf_files[i*3]),
                                            basename(acf_files[i*3 + 1]),
                                            basename(acf_files[i*3 + 2])))
        print('***')
    return acfs

def average_acfs(acfpath, acf_size):
    total_acf = np.zeros((acf_size))

    acf_files = glob(acfpath)
    print('len: ', len(acf_files))
    for acf_file in acf_files:
        total_acf += np.loadtxt(acf_file)[:,3]
        print('*')

    return total_acf / len(acf_files)

base_dir = "/Users/pboone/Dropbox (Personal)/Projects/LAMMPS Heat Flux Fix/LAMMPS run files/h1-hydrocarbons/c8h18-octane-emd-gk-72C/"
base_dir = "/Users/pboone/Dropbox (Personal)/Projects/LAMMPS Heat Flux Fix/LAMMPS run files/h1-hydrocarbons/c8h18-octane-emd-gk-72C-40A-5t/"
original_acfs = base_dir + "/acf_outputs/original/*.dat"
corrected_acfs = base_dir + "/acf_outputs/corrected/*.dat"

## 25.84 angstrom box
# volume = 25.84 ** 3
# temp = 344.96 # K
# experimental_k = 185.46

## 40 angstrom box
# volume = 40.00 ** 3
# temp = 345.17 # K
# experimental_k = 187.47

## 40 angstrom box 5t
volume = 40.00 ** 3
temp = 345.28 # K
nemd_k = 167.0
experimental_k = 187.40

orig_acfs = all_acfs(original_acfs, 100000)
corr_acfs = all_acfs(corrected_acfs, 100000)

avg_acfso = np.average(orig_acfs, axis=0)
avg_acfsi = np.average(corr_acfs, axis=0)


boltzmann_const = 1.3806504e-23 # J / K

kcal2j = 4186.0/6.02214e23  # kCal / mol to Joules
ang2m = 1.0e-10             # Angstroms to meters
fs2s = 1.0e-15              # Femtoseconds to seconds
convert = kcal2j**2 / (fs2s * ang2m) # kCal^2 / angstroms femtosecond => J / m s
sample_fs = 5

prefactor =  volume * convert * sample_fs / (boltzmann_const * temp**2)

all_indices = np.arange(0, 100000) / 1000 # convert to [ps]
datao = avg_acfso
datac = avg_acfsi

# plot_points = [1400, 8000] # 2.5ps, all data datao.shape[0]
plot_points = [1400, datao.shape[0]] # 7ps, all data


##### print ACF plots
### plot (1)
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('t [ps]')
ax.set_ylabel('ACF')
ax.grid(linestyle='-', color='0.7', zorder=0)

ax.set_xlim(0, 2)
# ax.set_ylim(-0.05, 0.05)

normalized_acfso = avg_acfso / avg_acfso[0]
normalized_acfsi = avg_acfsi / avg_acfsi[0]

ax.plot(all_indices * sample_fs, normalized_acfso, zorder=0, color="#FFBC75", lw=0.5, label="Original")
ax.plot(all_indices * sample_fs, normalized_acfsi, zorder=1, color="#AFC2FA", lw=0.5, label="Corrected")

save_figure_as_tiff(fig, "figures/acf_plot_0-2.tif", dpi=300)

### plot (2)
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('t [ps]')
ax.set_ylabel('ACF')
ax.grid(linestyle='-', color='0.7', zorder=0)
ax.set_xlim(0,500)
# ax.set_ylim(-0.05, 0.05)

np.average(avg_acfso[0:1000])
normalized_acfso = np.average(avg_acfso.reshape((100,1000)), axis=-1)
normalized_acfso /= avg_acfso[0]

normalized_acfsi = np.average(avg_acfsi.reshape((100,1000)), axis=-1)
normalized_acfsi /= avg_acfso[0]

normalized_indices = np.average(all_indices.reshape((100,1000)), axis=-1) * sample_fs

ax.plot(normalized_indices, normalized_acfso, zorder=0, color="#FFBC75", lw=0.5, label="Original")
ax.plot(normalized_indices, normalized_acfsi, zorder=1, color="#AFC2FA", lw=0.5, label="Corrected")

save_figure_as_tiff(fig, "figures/acf_plot_0-end.tif", dpi=300)

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
    integratedo = prefactor * cumtrapz(datao[:pp])
    integratedi = prefactor * cumtrapz(datac[:pp])

    print("Plot # %d" % plot_index)
    print("uncorrected: ", prefactor * simps(datao[:pp]))
    print("corrected: ", prefactor * simps(datac[:pp]))

    ax = fig.add_subplot(1, 2, plot_index + 1)

    ax.set_title(plot_labels[plot_index])
    ax.tick_params(axis='x', which='major', labelsize=fs)
    ax.tick_params(axis='y', which='major', labelsize=fs)
    ax.set_xlabel('($\\tau$ [ps]', fontsize=fsl)

    ax.set_ylabel('$\kappa$ [W / m K]', fontsize=fsl)
    # ax.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax.grid(linestyle='-', color='0.7', zorder=0)
    ax.plot(indices[:-1], integratedo, zorder=2, label="Uncorrected LAMMPS")
    ax.plot(indices[:-1], integratedi, zorder=2, label="Corrected")
    for i, one_traj_acf in enumerate(corr_acfs):
        int_one_traj = prefactor * cumtrapz(one_traj_acf[:pp])
        label = "Unaveraged corrected simulations" if i==0 else None
        ax.plot(indices[:-1], int_one_traj, zorder=0, color="#FFBC75", lw=0.5, label=label)

    for i, one_traj_acf in enumerate(orig_acfs):
        int_one_traj = prefactor * cumtrapz(one_traj_acf[:pp])
        label = "Unaveraged uncorrected simulations" if i==0 else None
        ax.plot(indices[:-1], int_one_traj, zorder=1, color="#AFC2FA", lw=0.5, label=label)

    ax.axhline(experimental_k / 1000, linestyle='dashed', linewidth=1, label="Experimental", color="black")
    ax.axhline(nemd_k / 1000, linestyle='dashed', linewidth=1, label="NEMD", color="0.4")
    ax.legend(fontsize=fsl)

save_figure_as_tiff(fig, "figures/acf_thermal_conductivity_two_ranges.tif", dpi=300)
