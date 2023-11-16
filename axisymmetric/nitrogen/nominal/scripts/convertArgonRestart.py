import numpy as np
import h5py as h5
import scipy.interpolate as spi

# Argon restart---we start with solution from this file
argonRestart = h5.File('../../../argon/highP/lte/restart_output-plasma-refine2.sol.h5', 'r')

# Nitrogen restart---and write to this file (after modifying)
# For simplicity, this file is assumed to already exist
nitrogenRestart = h5.File('../lte/restart_output-plasma-refine2.sol.h5', 'r+')

# Argon thermo property table (1-D version)
argonThermo = h5.File('../../../argon/lte-data/argon_thermo_1atm.h5', 'r')
TargonData = argonThermo['T_energy_R_c'][:,0]
eargonData = argonThermo['T_energy_R_c'][:,1]
RargonData = argonThermo['T_energy_R_c'][:,2]
argonThermo.close()

e_to_T_argon = spi.interp1d(eargonData, TargonData)
T_to_R_argon = spi.interp1d(TargonData, RargonData)

# Nitrogen thermo properties table (1-D version)
nitrogenThermo = h5.File('../../lte-data/nitrogen_thermo_1atm.h5', 'r')
TnitrogenData = nitrogenThermo['T_energy_R_c'][:,0]
enitrogenData = nitrogenThermo['T_energy_R_c'][:,1]
RnitrogenData = nitrogenThermo['T_energy_R_c'][:,2]

nitrogenThermo.close()

T_to_R_nitrogen = spi.interp1d(TnitrogenData, RnitrogenData)
T_to_e_nitrogen = spi.interp1d(TnitrogenData, enitrogenData)

# Extract argon solution, and compute temperature and pressure
rho_argon = argonRestart['/solution/density'][:]
ru_argon = argonRestart['/solution/rho-u'][:]
rv_argon = argonRestart['/solution/rho-v'][:]
rw_argon = argonRestart['/solution/rho-w'][:]
rE_argon = argonRestart['/solution/rho-E'][:]

# temperature from energy
ru2 = (ru_argon * ru_argon + rv_argon * rv_argon + rw_argon * rw_argon) / rho_argon
re_argon = rE_argon - 0.5 * ru2
e_argon = re_argon / rho_argon
T_argon = e_to_T_argon(e_argon)

# pressure
R_argon = T_to_R_argon(T_argon)
p_argon = rho_argon * R_argon * T_argon

# evaluate nitrogen state assuming velocity, temperature, and pressure from argon case
R_nitrogen = T_to_R_nitrogen(T_argon)
rho_nitrogen = p_argon / R_nitrogen / T_argon
e_nitrogen = T_to_e_nitrogen(T_argon)

ru_nitrogen = rho_nitrogen * (ru_argon / rho_argon)
rv_nitrogen = rho_nitrogen * (rv_argon / rho_argon)
rw_nitrogen = rho_nitrogen * (rw_argon / rho_argon)

ru2 = (ru_nitrogen * ru_nitrogen + rv_nitrogen * rv_nitrogen + rw_nitrogen * rw_nitrogen) / rho_nitrogen
rE_nitrogen = rho_nitrogen * e_nitrogen + 0.5 * ru2

# put into hdf5
nitrogenRestart['/solution/density'][:] = rho_nitrogen
nitrogenRestart['/solution/rho-u'][:] = ru_nitrogen
nitrogenRestart['/solution/rho-v'][:] = rv_nitrogen
nitrogenRestart['/solution/rho-w'][:] = rw_nitrogen
nitrogenRestart['/solution/rho-E'][:] = rE_nitrogen

nitrogenRestart.attrs['iteration'] = 0
nitrogenRestart.attrs['time'] = 0.0

nitrogenRestart.close()
argonRestart.close()
