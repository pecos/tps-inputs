import h5py
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants
import scipy.interpolate
import matplotlib
plt.style.use('ggplot')

font = {#'family' : 'normal',
        'weight' : 'bold',
        'size'   : 6}
matplotlib.rc('font', **font)

def rates_from_file(fname):
    with h5py.File(fname, "r") as f:
        ki = np.array(f["table"])
    
    ki_inp = scipy.interpolate.interp1d(ki[:,0], ki[:,1]/scipy.constants.Avogadro, bounds_error=False, fill_value=0)
    return ki_inp

rr_names    = {1: r"$e$ + $Ar$    $\rightarrow$  $e + Ar_m$", 
               2: r"$e$ + $Ar$    $\rightarrow$  $e + Ar_r$",
               3: r"$e$ + $Ar$    $\rightarrow$  $e + Ar_p$",
               5: r"$e$ + $Ar_m$  $\rightarrow$  $e + Ar^+$",
               6: r"$e$ + $Ar_r$  $\rightarrow$  $e + Ar^+$",
               7: r"$e$ + $Ar_p$  $\rightarrow$  $e + Ar^+$",
               }

mw_rates = [ rates_from_file("rate-coefficients/Excitation_Metastable.h5"),
             rates_from_file("rate-coefficients/Excitation_Resonant.h5"),  
             rates_from_file("rate-coefficients/Excitation_4p.h5"),
             rates_from_file("rate-coefficients/StepIonization_Metastable.h5"),
             rates_from_file("rate-coefficients/StepIonization_Resonant.h5"),
             rates_from_file("rate-coefficients/StepIonization_4p.h5")]

# mw_rates = [ rates_from_file("FullModel_1Torr/Excitation_Metastable.h5"),
#              rates_from_file("FullModel_1Torr/Excitation_Resonant.h5"),  
#              rates_from_file("FullModel_1Torr/Excitation_4p.h5"),
#              rates_from_file("FullModel_1Torr/StepIonization_Metastable.h5"),
#              rates_from_file("FullModel_1Torr/StepIonization_Resonant.h5"),
#              rates_from_file("FullModel_1Torr/StepIonization_4p.h5")]

bte_rates = np.genfromtxt("rate_bte/ss_ee_1_grid_03_rank_0_npes_1_qoi.csv",skip_header=1, delimiter=',')
Tg        = bte_rates[:, 6]
Tg_u      = np.unique(Tg)

ev1       = scipy.constants.Boltzmann/scipy.constants.electron_volt

plt.figure(figsize=(12, 6), dpi=300)
plt.subplot(1, 2, 1)
print(mw_rates[0](Tg_u))
plt.semilogy(ev1 * Tg_u, mw_rates[0](Tg_u), 'r', label=rr_names[1])
plt.semilogy(ev1 * Tg  , bte_rates[:, 12] , 'r', label=rr_names[1], lw=0, marker='o', fillstyle='none', markersize=2)

plt.semilogy(ev1 * Tg_u, mw_rates[1](Tg_u), 'b', label=rr_names[2])
plt.semilogy(ev1 * Tg  , bte_rates[:, 13] , 'b', label=rr_names[1], lw=0, marker='o', fillstyle='none', markersize=2)

plt.semilogy(ev1 * Tg_u, mw_rates[2](Tg_u), 'g', label=rr_names[3])
plt.semilogy(ev1 * Tg  , bte_rates[:, 14] , 'g', label=rr_names[1], lw=0, marker='o', fillstyle='none', markersize=2)

# plt.semilogy(Tg_u, mw_rates[3](Tg_u), 'r' , label=rr_names[5])
# plt.semilogy(Tg_u, mw_rates[4](Tg_u), 'b' , label=rr_names[6])
# plt.semilogy(Tg_u, mw_rates[5](Tg_u), 'g' , label=rr_names[7])


#plt.xlim(np.min(Tg), np.max(Tg))
plt.xlabel(r"temperature [K]")
plt.ylabel(r"rate coefficient [$m^3s^{-1}$]")
plt.legend()
plt.grid(visible=True)

plt.subplot(1, 2, 2)
plt.semilogy(ev1 * Tg_u, mw_rates[3](Tg_u), 'r' , label=rr_names[5])
plt.semilogy(ev1 * Tg  , bte_rates[:, 16] , 'r', label=rr_names[5], lw=0, marker='o', fillstyle='none', markersize=2)

plt.semilogy(ev1 * Tg_u, mw_rates[4](Tg_u), 'b' , label=rr_names[6])
plt.semilogy(ev1 * Tg  , bte_rates[:, 17] , 'b', label=rr_names[6], lw=0, marker='o', fillstyle='none', markersize=2)

plt.semilogy(ev1 * Tg_u, mw_rates[5](Tg_u), 'g' , label=rr_names[7])
plt.semilogy(ev1 * Tg  , bte_rates[:, 18] , 'g', label=rr_names[7], lw=0, marker='o', fillstyle='none', markersize=2)
plt.xlabel(r"temperature [K]")
plt.ylabel(r"rate coefficient [$m^3s^{-1}$]")
plt.legend()
plt.grid(visible=True)

plt.tight_layout()
plt.savefig("rates_comparison.png")
plt.show()