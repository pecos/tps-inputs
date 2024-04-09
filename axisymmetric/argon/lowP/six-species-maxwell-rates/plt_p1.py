import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.interpolate
import h5py
import scipy.constants
import matplotlib
matplotlib.rcParams.update({
      #"font.family": "serif",
      #"font.serif": [], # Use LaTeX default serif font.
      "text.usetex": True, # use inline math for ticks   ## You can change the font size of individual items with:
    #    "font.size": 14,
    #    "axes.titlesize": 14,
    #    "legend.fontsize": 14,
    #    "axes.labelsize": 14,
    })


folder_name = "rate_bte"
def compute_effective_ki(ki, ns_by_n0):
    return np.einsum("is,is->i", ki, ns_by_n0)

def rates_from_file(fname):
    with h5py.File(fname, "r") as f:
        ki = np.array(f["table"])
    
    ki_inp = scipy.interpolate.interp1d(ki[:,0], ki[:,1]/scipy.constants.Avogadro, bounds_error=False, fill_value=0)
    return ki_inp


d_arr      = np.genfromtxt("ionization_rates.csv", delimiter=",", skip_header=True)
ki_arr     = scipy.interpolate.interp1d(d_arr[:,0], d_arr[:,1], bounds_error=False, fill_value=0)
ki_max_3sp = scipy.interpolate.interp1d(d_arr[:,0], d_arr[:,2], bounds_error=False, fill_value=0)


bte_data   = [[np.genfromtxt("%s/ss_ee_0_grid_%02d_rank_0_npes_1_qoi.csv"%(folder_name, i), delimiter=",", skip_header=True) for i in range(4)],
              [np.genfromtxt("%s/ss_ee_1_grid_%02d_rank_0_npes_1_qoi.csv"%(folder_name, i), delimiter=",", skip_header=True) for i in range(4)],
              [np.genfromtxt("%s/ts_ee_0_grid_%02d_rank_0_npes_1_qoi.csv"%(folder_name, i), delimiter=",", skip_header=True) for i in range(4)],
              [np.genfromtxt("%s/ts_ee_1_grid_%02d_rank_0_npes_1_qoi.csv"%(folder_name, i), delimiter=",", skip_header=True) for i in range(4)]
              ]

bte_data_lbl = [r"Ar(6-SP) $E=E_0$", 
                r"Ar(6-SP) $E=E_0$ + $C_{ee}$", 
                r"Ar(6-SP) $E=E_0\exp(i\omega t)$", 
                r"Ar(6-SP) $E=E_0\exp(i\omega t)$ + $C_{ee}$", 
                ]

TG_IDX     = 6
E_IDX      = 7
NS_BY_N0   = list(range(2  ,  2 + 4))
G1_RATES   = list(range(12 , 12 + 3))
G2_RATES   = list(range(15 , 15 + 4))


g1_tab = [  rates_from_file("rate-coefficients/Excitation_Metastable.h5"),
            rates_from_file("rate-coefficients/Excitation_Resonant.h5"),
            rates_from_file("rate-coefficients/Excitation_4p.h5") ]

g2_tab = [  rates_from_file("rate-coefficients/Ionization.h5"),
            rates_from_file("rate-coefficients/StepIonization_Metastable.h5"),
            rates_from_file("rate-coefficients/StepIonization_Resonant.h5"),
            rates_from_file("rate-coefficients/StepIonization_4p.h5")]



GRID_IDX = list(range(3,4))
Tg1      = np.sort(np.unique(np.array([bte_data[0][grid_idx][:,TG_IDX] for grid_idx in GRID_IDX])))
k_to_ev  = (scipy.constants.Boltzmann/scipy.constants.electron_volt)

plt.figure(figsize=(6, 4))
plt.plot(Tg1 * k_to_ev , ki_arr(Tg1)     , label=r"Arrhenius")
#plt.plot(Tg1 * k_to_ev , ki_max_3sp(Tg1) , label=r"Maxwellian(3-SP)")

prop_cycle = plt.rcParams['axes.prop_cycle']
colors     = prop_cycle.by_key()['color']

for grid_idx in GRID_IDX:
    fname  = folder_name+"/effective_rate"
    Tg          = [bte_data[i][grid_idx][:,TG_IDX]    for i in range(len(bte_data))]
    E           = [bte_data[i][grid_idx][:,E_IDX]     for i in range(len(bte_data))]
    ns_by_n0    = [bte_data[i][grid_idx][:,NS_BY_N0]  for i in range(len(bte_data))]
    
    ki_g1       = [bte_data[i][grid_idx][:,G1_RATES]  for i in range(len(bte_data))]
    ki_g2       = [bte_data[i][grid_idx][:,G2_RATES]  for i in range(len(bte_data))]
    
    for i in range(1, len(bte_data)):
        assert np.allclose(Tg[0], Tg[i]) == True
        assert np.allclose(E[0] , E[i])  == True
        assert np.allclose(ns_by_n0[0] , ns_by_n0[i])  == True
    
    Tg       = Tg[0]
    ns_by_n0 = ns_by_n0[0]
    E        = E[0]
    
    
    for i in range(len(bte_data)):
        lbl          = bte_data_lbl[i]
        ki           = compute_effective_ki(ns_by_n0, ki_g2[i])
        
        plt.plot(Tg * k_to_ev , ki , lw=0, marker='o', fillstyle='none', markersize=3, color=colors[i], label=lbl)
    
    if(grid_idx==GRID_IDX[0]):
        plt.legend()
    
plt.yscale("log")
plt.xlabel(r"Temperature [eV]")
plt.ylabel(r"reaction rate [$m^3s^{-1}$]")
plt.grid(visible=True)
plt.tight_layout()
plt.savefig("%s.pgf"%(fname), format="pgf")
plt.savefig("%s.png"%(fname))
plt.close()


for m_idx in range(0, len(bte_data)):
    plt.figure(figsize=(6, 4))

    g1_lbl = [r"$Ar \rightarrow  Ar_m$", r"$Ar \rightarrow Ar_r$", r"$Ar \rightarrow Ar_p$"]
    g2_lbl = [r"$Ar \rightarrow Ar^+$" , r"$Ar_m \rightarrow Ar^+$", r"$Ar_r \rightarrow Ar^+$", r"$Ar_p \rightarrow Ar^+$"]

    if m_idx < 2:
        for i in range(len(g1_lbl)):
            plt.plot(Tg1 * k_to_ev, g1_tab[i](Tg1), color=colors[i] , label=g1_lbl[i])
        for i in range(len(g2_lbl)):
            plt.plot(Tg1 * k_to_ev, g2_tab[i](Tg1), color=colors[i + len(g1_lbl)], label=g2_lbl[i])
    
    
    for grid_idx in GRID_IDX:
        fname  = folder_name+"/effective_rate"
        Tg          = [bte_data[i][grid_idx][:,TG_IDX]    for i in range(len(bte_data))]
        E           = [bte_data[i][grid_idx][:,E_IDX]     for i in range(len(bte_data))]
        ns_by_n0    = [bte_data[i][grid_idx][:,NS_BY_N0]  for i in range(len(bte_data))]
        
        ki_g1       = [bte_data[i][grid_idx][:,G1_RATES]  for i in range(len(bte_data))]
        ki_g2       = [bte_data[i][grid_idx][:,G2_RATES]  for i in range(len(bte_data))]
        
        for i in range(1, len(bte_data)):
            assert np.allclose(Tg[0], Tg[i]) == True
            assert np.allclose(E[0] , E[i])  == True
            assert np.allclose(ns_by_n0[0] , ns_by_n0[i])  == True
        
        Tg       = Tg[0]
        ns_by_n0 = ns_by_n0[0]
        E        = E[0]
        
        for i in range(len(g1_lbl)):
            plt.plot(Tg * k_to_ev, ki_g1[m_idx][:, i], lw=0, marker='o', fillstyle='none', markersize=3, color=colors[i], label = g1_lbl[i])
        
        for i in range(len(g2_lbl)):
            plt.plot(Tg * k_to_ev, ki_g2[m_idx][:, i], lw=0, marker='o', fillstyle='none', markersize=3, color=colors[i + len(g1_lbl)], label = g2_lbl[i])
        
        if grid_idx == GRID_IDX[0]:
            plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fancybox=True,ncol=1, fontsize=11)
        
    plt.yscale("log")
    plt.xlabel(r"Temperature [eV]")
    plt.ylabel(r"reaction rate [$m^3s^{-1}$]")
    plt.tight_layout()
    
    plt.grid(visible=True)
    plt.savefig("%s_model_%02d.pgf"%(fname, m_idx), format='pgf')
    plt.savefig("%s_model_%02d.png"%(fname, m_idx))
    plt.close()


    


