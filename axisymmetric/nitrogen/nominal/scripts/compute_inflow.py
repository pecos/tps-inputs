# Comute the inflow conditions for 30 slpm of nitrogen
import numpy as np

# Modify here to change flow rate or geometric info
mdot_SLPM = 30 # nominal for nitrogen
Ro = 0.028067 # [m] outer radius of inlet slot
Ri = 0.022 # [m] inner radius of inlet slot

# Modify here to change the feed gas
Rgas = 296.803 # [J / (kg K)] (nitrogen)

# Should not need to modify below here, unless 'standard' conditions
# change (or use non-constant profile)

# standard conditions
p_standard = 101325 # [Pa] = 1 atm
T_standard = 298.15 # [K]
rho_standard = p_standard / (Rgas * T_standard)

Q = mdot_SLPM * 1e-3 / 60 # change LPM to m^3 / s
mdot = rho_standard * Q # Huzzah! now have kg / s
print("Mass flow rate = {0:.6e} [kg/s]".format(mdot))

inflow_area = np.pi * (Ro * Ro - Ri * Ri)
uaxial = mdot / rho_standard / inflow_area
print("Axial inflow velocity = {0:.6e} [m/s]".format(uaxial))

print("Inflow density = {0:.6e} [m/s]".format(rho_standard))
print("Inflow axial momentum = {0:.6e} [m/s]".format(rho_standard * uaxial))
