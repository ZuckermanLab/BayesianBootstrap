import scipy
import re
from bootstrap import get_CR

RunNums = 5
Rates = {}
MinVal = 10000  ### We replace all zeros with the smallest value measured

for run in range(1, RunNums + 1):
    Rates[run] = []
    Times = []  # will be overwritten at each iteration, but that's okay
    RUN = "{0:02}".format(run)
    FileIn = open("rate_" + RUN + ".dat")
    for line in FileIn.readlines():
        Words = line.split()
        if (len(Words) > 0) and (re.search("\d", Words[0])):
            Times.append(Words[0])
            Rates[run].append(float(Words[1]))
            if (float(Words[1]) < MinVal) and (float(Words[1]) > 0):
                MinVal = float(Words[1])
    FileIn.close()

FileOut_CR = open("AvgRates_CR.dat", 'w')

for i in range(len(Rates[1])):
    print("time step", i + 1, "/ ", len(Rates[1]))
    CurrData = []
    for run in range(1, RunNums + 1):
        CurrData.append(Rates[run][i])
    CurrAvg = scipy.average(CurrData)

    for j in range(len(CurrData)):
        if CurrData[j] == 0:  CurrData[j] = MinVal  ### We replace all zeros with the smallest value measured

    [CR_minval, CR_maxval] = get_CR(CurrData, 10000)  ### 10000-fold Bayesian bootstrapping performed

    # print >> FileOut_CR, Times[i], "\t", CurrAvg, "\t", CR_maxval, "\t", CR_minval
    print(FileOut_CR, Times[i], "\t", CurrAvg, "\t", CR_maxval, "\t", CR_minval)
