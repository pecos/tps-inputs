import numpy as np
import matplotlib.pyplot as plt

nrho = 1000
ntemp = 1000

D = np.loadtxt('nitrogen_transp_table.dat', skiprows=1)
Dt = np.loadtxt('nitrogen_thermo_table.dat', skiprows=1)

T = D[:,0].reshape((nrho, ntemp))
rho = D[:,1].reshape((nrho, ntemp))
mu = D[:,2].reshape((nrho, ntemp))
kappa = D[:,3].reshape((nrho, ntemp))
sigma = D[:,4].reshape((nrho, ntemp))

p = Dt[:,2].reshape((nrho, ntemp))

energy = Dt[:,3].reshape((nrho, ntemp))
R = Dt[:,6].reshape((nrho, ntemp))
c = Dt[:,8].reshape((nrho, ntemp))

# have max on table size, so skip every other point
ntemp = 500

# Extract quantities as a function of temperature at p = 1 atm
ptarg = 101325.

T_atm = np.zeros(ntemp)
rho_atm = np.zeros(ntemp)

sig_atm = np.zeros(ntemp)
kap_atm = np.zeros(ntemp)
mu_atm = np.zeros(ntemp)

energy_atm = np.zeros(ntemp)
R_atm = np.zeros(ntemp)
c_atm = np.zeros(ntemp)

for i in range(0, ntemp):
    ti = 2 * i

    # target temperature
    T_atm[i] = T[0,ti]

    # find indices of data points surrounding the target pressure
    ind = np.argmin(np.abs(p[:,ti] - ptarg))
    if (p[ind,ti] > ptarg):
        ind -= 1

    if (ind == nrho - 1):
        print(T_atm[i])
        ind -= 1

    plow = p[ind,ti]
    phig = p[ind+1,ti]
    dp = phig - plow
    w1 = (ptarg - plow) / dp
    w2 = (phig - ptarg) / dp

    # interpolate quantities to target pressure
    rho_atm[i] = rho[ind,ti] + w1 * (rho[ind+1,ti] - rho[ind,ti])

    sig_atm[i] = sigma[ind,ti] + w1 * (sigma[ind+1,ti] - sigma[ind,ti])
    kap_atm[i] = kappa[ind,ti] + w1 * (kappa[ind+1,ti] - kappa[ind,ti])
    mu_atm[i] = mu[ind,ti] + w1 * (mu[ind+1,ti] - mu[ind,ti])

    energy_atm[i] = energy[ind,ti] + w1 * (energy[ind+1,ti] - energy[ind,ti])
    R_atm[i] = R[ind,ti] + w1 * (R[ind+1,ti] - R[ind,ti])
    c_atm[i] = c[ind,ti] + w1 * (c[ind+1,ti] - c[ind,ti])


# plot transport
make_plots = True
if make_plots:
    plt.plot(T_atm, sig_atm, 'b-')
    plt.title("Electrical conductivity")
    plt.show()

    plt.plot(T_atm, kap_atm, 'b-')
    plt.title("Thermal conductivity")
    plt.show()

    plt.plot(T_atm, mu_atm, 'b-')
    plt.title("Dynamic viscosity")
    plt.show()

# save data
transport_data = np.stack((T_atm, mu_atm, kap_atm, sig_atm), axis=1)

import h5py as h5
F = h5.File("nitrogen_transport_1atm.h5", "w")
F.create_dataset("T_mu_kappa_sigma", data=transport_data, dtype='d')
F.close()


thermo_data = np.stack((T_atm, energy_atm, R_atm, c_atm), axis=1)

import h5py as h5
F = h5.File("nitrogen_thermo_1atm.h5", "w")
F.create_dataset("T_energy_R_c", data=thermo_data, dtype='d')
F.close()
