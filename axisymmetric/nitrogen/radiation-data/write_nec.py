import numpy as np
import matplotlib.pyplot as plt
import h5py as h5

fileroot=['nitrogen_nec_R100p0mm',
          'nitrogen_nec_R010p0mm',
          'nitrogen_nec_R001p0mm',
          'nitrogen_nec_R000p1mm',
          'nitrogen_nec_R000p0mm']

for f in fileroot:
    D = np.loadtxt(f+'.csv', delimiter=',')

    # extrapolate to lower temperatures
    Tlow = np.linspace(1000, 4000, 7)
    alfa = 2.493061e+01
    lC = -2.048356e+02
    elow = np.exp(lC) * Tlow**alfa
    Dlow = np.stack((Tlow, elow), axis=1)
    Dall = np.vstack((Dlow, D))

    F = h5.File(f+'.h5', 'w')
    F.create_dataset("table", data=Dall)

    F.attrs.create("name0", data="Temperature")
    F.attrs.create("name1", data="Net emission coefficient (nitrogen)")
    F.attrs.create("unit0", data="K")
    F.attrs.create("unit1", data="W/m3/sr")
    F.attrs.create("Reference", data="https://dx.doi.org/10.1088/0022-3727/35/22/306")
    F.close()

