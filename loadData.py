from numpy import array, concatenate, nanmean, reshape, transpose
from math import *
from csv import reader
from os import getcwd
from os.path import join, split
import numpy as np
import warnings

def converter(x):
    try:
        return float(x)
    except ValueError:
        return np.nan

def loadData():
    ## To begin, read in the MFI measurements from both of Lux's experiments from
    ## their respective csvs. Then, subtract background MFIs from these nominal
    ## MFIs. Then, normalize the data by replicate. For each step after the
    ##reading, I manipulated the csv data in different ways, which are explained
    ## in the comments. Please refer to these comments to understand what is
    ## going on, especially with variables of the name "book$" or "temp$." All
    ## variables with such names are only meant to construct mfiAdjMean1 (from
    ## Lux's first experiments) and mfiAdjMean2 (from Lux's second experiments).

    ## mfiAdjMean1:
    ## Find path for csv files, on any machine wherein the repository recepnum1 exists.
    path = './Nimmerjahn Lab and Bruhns Data'
    ## Read in the csv data for the first experiments. lux1 is an iterable data
    ## structure wherein each iterable element is a single-element list containing a
    ## string. Each such string represents a single row from the csv.
    book4 = np.loadtxt(join(path,'Luxetal2013-Fig2B.csv'),\
        converters = {2: converter}, delimiter=',', skiprows=2, \
        usecols=list(range(2,10)))

    ## The first row in every set of five rows in book4 consists of background
    ## MFIs. book5 is made by taking each of the four non-background MFIs from
    ## reach cluster of 5 from book4, subtracting the corresponding background
    ## MFI from each, and then forming a NumPy array of shape (24,8) from all of
    ## these collectively. The final result, book5, will be a NumPy array of
    ## shape (1,192).
    book5 = array([])
    for j in range(len(book4)):
        if j%5 == 0:
            temp = array(book4[j])
        else:
            temp2 = array(book4[j])-temp
            book5 = concatenate((book5,temp2),0)
    ## Reshape book5 into a NumPy array of shape (24,8), the actual shape of the
    ## MFIs from Lux's original experiments.
    book5 = reshape(book5,(24,8))
    ## Transponse book5, so that all the elements in rows n and n+4 correspond to
    ## the same replicate (for all n in {0,1,2,3}; Python indexing used). Then,
    ## concatenate both rows in a single replicate, and take the mean of the
    ## resulting array. This mean will correspond to the normalizing factor by
    ## which the corresponding replicate is normalized. These are first contained
    ## the (1,4) NumPy array means.
    temp = transpose(book5)
    means = [nanmean(concatenate((temp[j],temp[j+4]))) for j in range(4)]
    ## Concatenate means with itself to result in a (1,8) NumPy array, means2
    means2 = concatenate((means,means))
    ## Concatenate means2 with itself until a NumPy array of shape (1,192) is
    ## created. This array is titled "temp." Then, reshape temp into a (24,8)
    ## NumPy array called "noise." Each element in book5 must be divided by the
    ## corresponding element in temp in order to be normalized.
    temp = means2
    for j in range(book5.shape[0]-1):
        temp = concatenate((temp,means2))
    noise = reshape(temp,(24,8))
    ## Create mfiAdjMean1 by dividing book5 by noise.
    mfiAdjMean1 = book5/noise

    ## mfiAdjMean2:
    ## Read in the csv data for the first experiments. lux2 is an iterable data
    ## structure wherein each iterable element is a single-element list
    ## contraining a string. Each such string represents a single row from the
    ## csv.
    book5 = np.loadtxt(join(path,'New-Fig2B.csv'),\
        converters = {2: converter}, delimiter=',', skiprows=2, \
        usecols=list(range(2,10)))
    ## The first row in every set of five rows in book5 consists of background
    ## MFIs. book6 is made by taking each of the four non-background MFIs from
    ## reach cluster of 5 from book5, subtracting the corresponding background
    ## MFI from each, and then forming a NumPy array of shape (20,8) from all of
    ## these collectively. The final result, book5, will be a NumPy array of
    ## shape (1,160).
    book5 = array(book5)
    book6 = array([])
    for j in range(len(book5)):
        if j%5 == 0:
            temp = array(book5[j])
        else:
            temp2 = array(book5[j])-temp
            book6 = concatenate((book6,temp2),0)
    ## Reshape book6 into an array of shape (20,8).
    book6 = reshape(book6,(24,8))

    #print(book6)
    ## Transponse book6, so that all the elements in rows n and n+4 correspond
    ## to the same replicate (for all n in {0,1,2,3}; Python indexing used).
    ## Then, concatenate both rows in a single replicate, and take the mean of
    ## the resulting array. This mean will correspond to the normalizing factor
    ## by which the corresponding replicate is normalized. These are first
    ## contained the (1,4) NumPy array means.
    temp = transpose(book6)
    means = [nanmean(concatenate((temp[j],temp[j+4]))) for j in range(4)]
    ## Concatenate means with itself to result in a (1,8) NumPy array, means2
    means2 = concatenate((means,means))
    ## Concatenate means2 with itself until a NumPy array of shape (1,192) is
    ## created. This array is titled "temp." Then, reshape temp into a (24,8)
    ## NumPy array called "noise." Each element in book6 must be divided by the
    ## corresponding element in temp in order to be normalized.
    temp = means2
    for j in range(book6.shape[0]-1):
        temp = concatenate((temp,means2))
    noise = reshape(temp,(24,8))
    ## Create mfiAdjMean2 by dividing book6 by noise.
    mfiAdjMean2 = book6/noise

    ## Make mfiAdjMean2 of shape (24,8) by inserting a (4,8) array of NaNs where the
    ## FcgRIIA-Arg data would otherwise be.
    mfiAdjMean2 = concatenate((mfiAdjMean2[0:4,:],np.nan*np.ones((4,8)),mfiAdjMean2[4:20,:]))

    ## Define concentrations of TNP-4-BSA and TNP-26-BSA
    ## These are put into the numpy array "tnpbsa"
    tnpbsa4 = 1/67122*1e-3*5
    tnpbsa26 = 1/70928*1e-3*5
    tnpbsa = array([tnpbsa4,tnpbsa26])

    ## Define the matrix of Ka values from Bruhns
    ## For accuracy, the Python implementation of this code will use
    ## Ka values as opposed to Kd, as these were the values which Bruhns
    ## gives in his experiments. These are read in from a csv in the
    ## folder Nimmerjahn Lab and Bruhns Data. Each row represents a particular
    ## FcgR (FcgRIA, FcgRIIA-H, FcgRIIA-R, FcgRIIB, FcgRIIIA-F, FcgRIIIA-V)
    ## and each column represents a particular IgG(1, 2, 3, 4).

    ## First, read in the csv. It will result in an iterable object, wherein
    ## each element is a single-element list containing a single string, each
    ## string corresponding to a single row from the csv.
    kaBruhns = np.loadtxt(join(path,'FcgR-Ka-Bruhns.csv'),\
        converters = {1: converter}, delimiter=',')

    ## Create the NumPy array Rquant, where each row represents a particular
    ## IgG (1,2,3, or 4) and each column corresponds to a particular FcgR
    ## (FcgRIA, FcgRIIA-H,FcgRIIA-R, FcgRIIB, FcgRIIIA-F, and FcgRIIIA-V)

    ## Read in the receptor quantifications for the Nimmerjahn Lab's second
    ## set of data. Using the function reader from the csv library, this data
    ## is used to make the iterable object quant, each iterable element of
    ## which is a single-element list containing a string corresponding to
    ## a row in the original csv.
    Rquant = np.loadtxt(join(path,'FcgRquant.csv'),\
        converters = {0: converter, 1: converter, 4: converter, 5: converter}, \
        delimiter=',', skiprows=1)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        Rquant = np.nanmean(Rquant, axis=0)

    return {'mfiAdjMean1':mfiAdjMean1, 'tnpbsa':tnpbsa, 'kaBruhns':kaBruhns, \
            'mfiAdjMean2':mfiAdjMean2, 'Rquant':Rquant}
