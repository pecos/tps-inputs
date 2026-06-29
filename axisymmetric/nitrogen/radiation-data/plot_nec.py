import numpy as np
import matplotlib.pyplot as plt
import h5py as h5

fileroot=['nitrogen_nec_R100p0mm',
          'nitrogen_nec_R010p0mm',
          'nitrogen_nec_R001p0mm',
          'nitrogen_nec_R000p1mm',
          'nitrogen_nec_R000p0mm']

for f in fileroot:
    F = h5.File(f+'.h5', 'r')
    D = F['table'][:,:]

    # b = np.array([np.log(D[0,1]), np.log(D[1,1])])
    # A = np.ones((2,2))
    # A[0,0] = np.log(D[0,0])
    # A[1,0] = np.log(D[1,0])

    # x = np.linalg.solve(A,b)
    # alfa = x[0]
    # lC = x[1]
    # print('alfa = {0:.6e}, lc = {1:.6e}'.format(alfa, lC))

    # Dp = np.zeros((D.shape[0]+1, D.shape[1]))
    # Dp[0,0] = 1000.
    # Dp[1:,0] = D[:,0]
    # Dp[0,1] = np.exp(lC) * 1000.0**alfa
    # Dp[1:,1] = D[:,1]

    #plt.loglog(D[:,0], D[:,1], '-x', label=f)
    plt.semilogy(D[:,0], D[:,1], '-x', label=f)
    #plt.plot(D[:,0], D[:,1], '-x', label=f)
    #plt.ylim(0, 1e5)

plt.legend()
plt.show()
