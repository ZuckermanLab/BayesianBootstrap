import scipy
import re

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bootstrap import get_CR

RunNums = 5
Rates = {}
# We replace all zeros with the smallest value measured
MinVal = 10000

# Populate the Rates dictionary with data from rate_0{1..5}.dat
for run in range(1, RunNums + 1):
    Rates[run] = []
    Times = []  # will be overwritten at each iteration, but that's okay
    RUN = "{0:02}".format(run)
    with open("rate_" + RUN + ".dat") as FileIn:
        for line in FileIn.readlines():
            Words = line.split()
            if (len(Words) > 0) and (re.search("\d", Words[0])):
                Times.append(Words[0])
                Rates[run].append(float(Words[1]))
                if (float(Words[1]) < MinVal) and (float(Words[1]) > 0):
                    MinVal = float(Words[1])


with open("AvgRates_CR.dat", 'w') as FileOut_CR:

    for i in range(len(Rates[1])):
        print("time step", i + 1, "/ ", len(Rates[1]))
        CurrData = []
        for run in range(1, RunNums + 1):
            CurrData.append(Rates[run][i])
        CurrAvg = scipy.average(CurrData)

        # We replace all zeros with the smallest value measured
        for j in range(len(CurrData)):
            if CurrData[j] == 0:  CurrData[j] = MinVal

        # 10000-fold Bayesian bootstrapping performed
        [CR_minval, CR_maxval] = get_CR(CurrData, 10000)

        # Just do it this way with redirecting stdout for consistency with the original implementation.
        #   Not the cleanest way
        original_stdout = sys.stdout
        sys.stdout = FileOut_CR
        print(FileOut_CR, Times[i], "\t", CurrAvg, "\t", CR_maxval, "\t", CR_minval)
        sys.stdout = original_stdout
