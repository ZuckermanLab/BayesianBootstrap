#!/usr/bin/python

import scipy
import random

def get_CI(List, Repeat):
    # NO CI if List has only identical elements
    if len(set(List)) == 1:
        return [0, 0]

    else:
        # List of data(!) sample means for every bootstrap iteration
        AllMeans = []
        # Number of data points
        N = len(List)

        # Repeated bootstrap iterations
        for i in range(Repeat):
            # Sample list
            CurrList = []
            for j in range(N):
                CurrList.append(random.choice(List))
            AllMeans.append(scipy.average(CurrList))

        # Minimum percentile defined over list of means
        perc_min = scipy.percentile(AllMeans, 2.5)
        # Maximum percentile defined over list of means
        perc_max = scipy.percentile(AllMeans, 97.5)

        # Confidence Interval is defined by min/max percentiles of sampling means
        return [perc_min, perc_max]


def get_CR(List, Repeat):
    """
    Compute a credibility region based on Bayesian bootstrapping of the input data.

    :param List: 1-dimensional array-like of input data

    :param Repeat: Number of bootstrap iterations to perform

    :return: (lower CR limit, upper CR limit)
    """


    # Test for identical elements by casting as a set.
    #   NO CR if List has only identical elements
    if len(set(List)) == 1:
        return [0, 0]

    else:
        # List of model(!) sample means for every bootstrap iteration
        AllMeans = []
        # Number of data points
        N = len(List)

        # Repeated bootstrap iterations
        for i in range(Repeat):

            # Following Rubin et al. to get data probabilities from Dirichlet distrib.
            Rands = [0]
            CurrAvg = 0
            for j in range(N - 1):
                Rands.append(random.random())
            Rands.append(1)
            Rands.sort()

            # List of random numbers that add to 1 and are used as data probabilities
            P = scipy.diff(Rands)
            for j in range(N):
                CurrAvg += P[j] * List[j]  # Sample mean
            AllMeans.append(CurrAvg)

        AllMeans.sort()
        TotalProb = len(AllMeans)
        CumulProb = 0
        perc_min = 0
        perc_max = 0
        # Iterating through sorted means, identifying that mean at which a certain percentile of probs is reached
        for m in AllMeans:
            CumulProb += 1
            if (CumulProb > 0.025 * TotalProb) and (perc_min == 0):
                perc_min = m
            if (CumulProb > 0.975 * TotalProb) and (perc_max == 0):
                perc_max = m

    # Credibility Region is defined by min/max percentiles of sampling means
    return [perc_min, perc_max]
