from bootstrap import *
import numpy as np
import matplotlib.pyplot as plt

n_runs = 5

# grab rate column (1) only
rates = [np.loadtxt(f"rate_0{i}.dat")[:,1] for i in range(1, n_runs + 1)]
# array of the 5 rate arrays
rates = np.array(rates)

# min non-zero value
min_val = np.amin(rates[np.nonzero(rates)])
# replace all zeros with smallest value measured
rates[rates == 0] = min_val

# get mean array of n replicates at each timepoint
means = np.average(rates, axis=0)
# calculate CRs at each timepoint
CRs = get_CR_multi(rates, 100)

# plotting
plt.plot(means)
plt.fill_between([i for i in range(0,rates.shape[1])], CRs[:,0], CRs[:,1], alpha=0.2)
plt.plot(np.rot90(rates))
plt.yscale("log", subs=[2, 3, 4, 5, 6, 7, 8, 9])
plt.show()