
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from scipy.integrate import cumtrapz, simps

def average_acfs(acfpath, acf_size):
    total_acf = np.zeros((acf_size))

    acf_files = glob(acfpath)
    print('len: ', len(acf_files))
    for acf_file in acf_files:
        total_acf += np.loadtxt(acf_file)[:,3]
        print('*')

    return total_acf / len(acf_files)

base_dir = "/Users/pboone/Dropbox (Personal)/Projects/LAMMPS Heat Flux Fix/LAMMPS run files/h1-hydrocarbons/c8h18-octane-emd-gk-72C/"
original_acfs = base_dir + "/acf_outputs/original/*"
corrected_acfs = base_dir + "/acf_outputs/corrected/*"

avg_acfso = average_acfs(original_acfs, 20000)
avg_acfsi = average_acfs(corrected_acfs, 20000)

# " V / (Kb * T^2): Volume / (boltzmann factor * temp squared)"
temp = 345.15 # K
volume = np.prod(-1*(np.array((-0.042139, 0.037034, -0.270039)) - (25.797861, 25.877034, 171.999965)))
boltzmann_const = 1.3806504e-23 # J / K

kcal2j = 4186.0/6.02214e23  # kCal / mol to Joules
ang2m = 1.0e-10             # Angstroms to meters
fs2s = 1.0e-15              # Femtoseconds to seconds
convert = kcal2j**2 / (fs2s * ang2m) # kCal^2 / angstroms femtosecond => J / m s
sample_fs = 5

prefactor =  volume * convert * sample_fs / (boltzmann_const * temp**2)

all_indices = np.arange(0,20000) / 1000 # convert to [ps]
datao = avg_acfso
datac = avg_acfsi

plot_points = [500, datao.shape[0]] # 2.5ps, all data
plot_labels = ("(A)", "(B)")
plot_label_pos = (0.10, 0.60)

rcParams.update({'figure.autolayout': True})

fs = 7
fsl = fs
fig = plt.figure(figsize=(7,3), dpi=600, tight_layout=True)

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
    # fig.text(plot_label_pos[plot_index], 0.05, plot_labels[plot_index], fontsize=fsl, weight="bold")
    ax.tick_params(axis='x', which='major', labelsize=fs)
    ax.tick_params(axis='y', which='major', labelsize=fs)
    ax.set_xlabel('($\\tau$ [ps]', fontsize=fsl)

    ax.set_ylim(0,0.7)
    ax.set_ylabel('$\kappa$ [W / m s]', fontsize=fsl)
    # ax.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax.grid(linestyle='-', color='0.7', zorder=0)
    ax.plot(indices[:-1], integratedo, zorder=2, label="Uncorrected LAMMPS")
    ax.plot(indices[:-1], integratedi, zorder=2, label="Corrected")
    ax.axhline(0.18977, linestyle='dashed', linewidth=1, label="Experimental", color="black")
    ax.legend(fontsize=fsl)

fig.savefig("acf_thermal_conductivity.png", dpi=600)
