#!/usr/bin/python

#import scipy
import random
import numpy as np
from tqdm.auto import tqdm

################################################
############## DEFINING CI FUNCTION ############
################################################

def get_CI(List, Repeat):
    """
    Standard bootstrapping CIs.
    """
    if len(set(List)) == 1 :  	# NO CI if List has only identical elements
        return [0,0]

    else :
        AllMeans = []		# List of data(!) sample means for every bootstrap iteration
        N = len(List)                # Number of data points

        for i in range(Repeat) :	# Repeated bootstrap iterations
            CurrList = []		# Sample list
            for j in range(N) :
                CurrList.append(random.choice(List))
            AllMeans.append(np.average(CurrList))

    perc_min  = np.percentile(AllMeans,2.5)	# Minimum percentile defined over list of means 
    perc_max  = np.percentile(AllMeans,97.5) 	# Maximum percentile defined over list of means

    return [perc_min, perc_max]	# Confidence Interval is defined by min/max percentiles of sampling means


################################################
############## DEFINING CR FUNCTION ############
################################################

def get_CR_bm(List, Repeat):
    """
    Original bayesian bootstrapping function from BM.
    """
    if len(set(List)) == 1 :  	# NO CR if List has only identical elements
        return [0,0]

    else :
        AllMeans = []		# List of model(!) sample means for every bootstrap iteration
        N = len(List)		# Number of data points

        for i in range(Repeat) :	# Repeated bootstrap iterations
            Rands = [0]		# Following Rubin et al. to get data probabilities from Dirichlet distrib.
            CurrAvg = 0
            for j in range(N-1) :
                Rands.append(random.random()) 
            Rands.append(1)
            Rands.sort()
            P=np.diff(Rands)	# List of random numbers that add to 1 and are used as data probabilities
            for j in range(N) :
                CurrAvg += P[j]*List[j]	# Sample mean
            AllMeans.append(CurrAvg)		
    
    AllMeans.sort()
    TotalProb = len(AllMeans)
    CumulProb = 0
    perc_min  = 0
    perc_max  = 0
    for m in AllMeans :	# Iterating through sorted means, identifying that mean at which a certain percentile of probs is reached
        CumulProb += 1
        if (CumulProb > 0.025*TotalProb) and (perc_min == 0) :
            perc_min = m   
        if (CumulProb > 0.975*TotalProb) and (perc_max == 0):
            perc_max = m

    return [perc_min, perc_max]		# Credibility Region is defined by min/max percentiles of sampling means 

#####################################################################
################## Updated functions using numpy ####################
#####################################################################

def get_CR_single(rates, repeat):
    """
    Get a set of min and max credibility regions (CRs) from bayesian
    bootstrapping for a 1d array of n_replicates at a single timepoint.

    Parameters
    ----------
    rates : 1darray
        Rates of each replicate at a single timepoint.
    repeat : int
        n-fold bayesian bootstrapping.

    Returns
    -------
    CRs : 1darray (min CR | max CR)
        2 item array of calculated min and max CRs for the input rates array.
    """
    # check if all elements in the rates array are identical
    if np.unique(rates).size == 1:
        return np.array([0, 0])

    else:
        all_means = np.zeros(repeat)

        # n-fold (n repeat) bayesian bootstrapping
        for i in range(repeat):
            # get data probabilities from Dirichlet distrib.
            rands = np.random.dirichlet(np.ones(len(rates)))
            # calculate the sample mean using dot product
            all_means[i] = np.dot(rands, rates)

        # identifying the sorted mean at which a certain percentile of probs is reached
        all_means.sort()
        total_prob = repeat
        cumul_prob = np.arange(1, total_prob + 1)
        # calculate the percentile values
        perc_min = all_means[np.argmax(cumul_prob > 0.025 * total_prob)]
        perc_max = all_means[np.argmax(cumul_prob > 0.975 * total_prob)]

        return np.array([perc_min, perc_max])

def get_CR_multi(rates_multi, repeat):
    """
    Calculate the credibility regions of multiple timepoints.
    Input `rates_multi` array should have n_replicate rows and
    n_timepoints columns.

    Parameters
    ----------
    rates_multi : 2darray
        Rates for multiple replicates at multiple timepoints.
    repeats : int
        n-fold bayesian bootstrapping.
    
    Returns
    -------
    CRs : 2darray
        Calculated min and max CRs for n_replicates at each timepoint.
        n_timepoints rows and 2 columns (min CR and max CR).
    """
    # CRs will be 2 columns (min and max) and n_frames rows
    CRs = np.zeros((rates_multi.shape[1], 2))
    # loop each timepoint, so each set of n_replicate rates, must transpose
    for i, rep_rates in enumerate(tqdm(rates_multi.T)):
        CRs[i,:] = get_CR_single(rep_rates, repeat)
    return CRs

# check the updated numpy version works
# rates = [0.02, 0.005, 0.033]
# print(get_CR_bm(rates, 10000))
# print(get_CR_single(rates, 10000))