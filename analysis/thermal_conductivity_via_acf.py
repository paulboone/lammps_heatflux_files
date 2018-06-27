
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumtrapz, simps

def average_acfs(acfpath, acf_size):
    total_acf = np.zeros((acf_size))
    for i, acffile in enumerate(glob(acfpath)):
        total_acf += np.loadtxt(acffile)[:,3]

    print(i + 1)
    return total_acf / (i + 1)


base_dir = "/Users/pboone/Dropbox (Personal)/Projects/LAMMPS Heat Flux Fix/LAMMPS run files/h1-hydrocarbons/c8h18-octane-emd-gk/"
original_acfs = base_dir + "/acf_outputs/original/*"
corrected_acfs = base_dir + "/acf_outputs/corrected/*"

avg_acfso = average_acfs(original_acfs, 20000)
avg_acfsi = average_acfs(corrected_acfs, 20000)

# " V / (Kb * T^2): Volume / (boltzmann factor * temp squared)"
temp = 401.87 # K
volume = np.prod(-1*(np.array((-0.042139, 0.037034, -0.270039)) - (25.7979, 25.877, 172)))
boltzmann_const = 1.3806504e-23 # J / K

kcal2j = 4186.0/6.02214e23  # kCal / mol to Joules
ang2m = 1.0e-10             # Angstroms to meters
fs2s = 1.0e-15              # Femtoseconds to seconds
convert = kcal2j**2 / (fs2s * ang2m) # kCal^2 / angstroms femtosecond => J / m s
sample_fs = 5

prefactor =  volume * convert * sample_fs / (boltzmann_const * temp**2)

indices = np.arange(0,20000) / 1000 # convert to [ps]
datao = avg_acfso
datac = avg_acfsi

plot_points = datao.shape[0]
plot_points = 500

indices = indices[:plot_points] * sample_fs
integratedo = prefactor * cumtrapz(datao[:plot_points])
integratedi = prefactor * cumtrapz(datac[:plot_points])
# simps(datao[:plot_points])
# simps(datac[:plot_points])
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('$\\tau$ [ps]')

# ax.set_ylim(0,6e-11)
ax.set_ylabel('$\kappa$ [W / m s]')
ax.grid(linestyle='-', color='0.7', zorder=0)
ax.plot(indices[:-1], integratedo, zorder=2, label="original")
ax.plot(indices[:-1], integratedi, zorder=2, label="corrected")
ax.legend()


fig.savefig("acf_thermal_conductivity_10ps.png", dpi=288)

# ax2 = ax.twinx()
# ax.plot(indices, datao[:plot_points] / volume, zorder=2)
# ax.plot(indices, datac[:plot_points] / volume, zorder=2)
# ax.set_ylabel('Heat flux auto correlation function [Kcal / mol A^2 fs]')
# ax.set_ylim(-1e-15,10e-15)




# ax.set_xlim(0,t_end)
# ax.legend(['C_a'])
# ax.set_title('Concentration vs Time' + subheader)
# fig.savefig("conc-vs-time.png", dpi=288)
