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
    path = split(getcwd())[0]+'/recepnum1/Nimmerjahn Lab and Bruhns Data'
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
    Fig2B = open(join(path,'New-Fig2B.csv'),newline = '')
    lux2 = reader(Fig2B,delimiter = ' ', quotechar = '|')
    ## Iterate over each list in lux2, appending each list to the list book.
    book = []
    for row in lux2:
        book.append(row)
    ## Rows 1 and 2 from the csv are only text; create the new list book2 which
    ## contains only rows 3 through 32 of book.
    book2 = []
    for j in range(2,32):
        book2.append(book[j][0])
    ## From each string in book2, create an individual string for each element in
    ## the original csv. In book3, each string in book2 corresponds to a list of
    ## these smaller strings.
    book3 = []
    for string in book2:
        temp = []
        temp2 = ''
        for j in range(len(string)):
            if string[j] != ',':
                temp2 = temp2+string[j]
            else:
                temp.append(temp2)
                temp2 = ''
        temp.append(temp2)
        book3.append(temp)
    ## Covert all strings in book4 to floats, where applicable. All strings with
    ## alphabetical characters are skipped over; no float is created for these.
    ## This results in the list book4, wherein each element is a list
    ## containing eight floats, save the second-to-last element, which
    ## contains seven.
    book4 = []
    for row in book3:
        temp = []
        for elem in row:
            try:
                temp.append(float(elem))
            except ValueError:
                a = 6
        book4.append(temp)

    ## In book4, due to there being data lost from the FcgRIIA-R experimentation,
    ## the rows corresponding to this group are all empty lists. Therefore, book5
    ## Is identical to book4, save for that the elements of length 0 are excluded.
    book5 = []
    for row in book4:
        if len(row) == 8:
            book5.append(row)

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
    book6 = reshape(book6,(20,8))

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
    noise = reshape(temp,(20,8))
    ## Create mfiAdjMean2 by dividing book6 by noise.
    mfiAdjMean2 = book6/noise

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

    ## Create a matrix which contains the mean value for each condition
    ## (after mean adjustment) from Lux's first experiments of the size
    ## 24x2

    meanPerCond1 = []
    for j in range(24):
        temp = []
        for k in range(2):
            temp2 = []
            for l in range(4):
                temp2.append(mfiAdjMean1[j,k*4+l])
            temp.append(nanmean(array(temp2)))
        meanPerCond1.append(temp)
    meanPerCond1 = array(meanPerCond1)

    ## Create a matrix which contains the mean value for each condition
    ## (after mean adjustment) from Lux's second experiments of the size
    ## 20x2

    meanPerCond2 = []
    for j in range(20):
        temp = []
        for k in range(2):
            temp2 = []
            for l in range(4):
                temp2.append(mfiAdjMean2[j,k*4+l])
            temp.append(nanmean(array(temp2)))
        meanPerCond2.append(temp)
    meanPerCond2 = array(meanPerCond2)

    ## Create the NumPy array Rquant, where each row represents a particular
    ## IgG (1,2,3, or 4) and each column corresponds to a particular FcgR
    ## (FcgRIA, FcgRIIA-H,FcgRIIA-R, FcgRIIB, FcgRIIIA-F, and FcgRIIIA-V)

    ## Read in the receptor quantifications for the Nimmerjahn Lab's second
    ## set of data. Using the function reader from the csv library, this data
    ## is used to make the iterable object quant, each iterable element of
    ## which is a single-element list containing a string corresponding to
    ## a row in the original csv.
<<<<<<< HEAD
    quantDoc = open(join(path,'FcgRquant.csv'),newline='')
    quant = reader(quantDoc,delimiter = ' ', quotechar = '|')
    ## Create a list book which contains all of the lists from quant
    book = []
    for row in quant:
        book.append(row)
    ## Remove the first element from book, which is only a string corresponding
    ## to the names of the receptor species. Also, convert each single-element
    ## list (containing a single string) in book to that list's single element
    ## (the string). Each list in book2 corresponds to its respective list in
    ## book in regards to this conversion.
    book2 = []
    for j in range(1,len(book)):
        book2.append(book[j][0])
    ## Convert every single-element list into a list of smaller strings, where
    ## each string corresponds to an element of the original csv. book3 is a
    ## list corresponding to book such that each list in book3 is made of the
    ## substrings of the string in the corresponding single-element list of book2.
    book3 = []
    for string in book2:
        temp = []
        temp2 = ''
        for j in range(len(string)):
            if string[j] != ',':
                temp2 = temp2+string[j]
            else:
                temp.append(temp2)
                temp2 = ''
        temp.append(temp2)
        book3.append(temp)
    ## Convert every string in book3 to a float, wherein possible. All strings
    ## equal to '' are turned into float nans. These transformations account
    ## for all the strings in book3.
    for j in range(len(book3)):
        for k in range(len(book3[0])):
            try:
                book3[j][k] = float(book3[j][k])
            except ValueError:
                book3[j][k] = nan
    ## Create Rquant by converting book3 to a NumPy array
    Rquant = array(book3)

    ## Create a list of tuples RquantTups, each tuple corresponding to the
    ## indices of a non-nan float in Rquant.
    RquantTups = []
    for j in range(len(Rquant)):
        for k in range(len(Rquant[0])):
            if not isnan(Rquant[j][k]):
                RquantTups.append((j,k))
=======
    Rquant = np.loadtxt(join(path,'FcgRquant.csv'),\
        converters = {0: converter, 2: converter, 4: converter, 5: converter}, \
        delimiter=',', skiprows=1)
>>>>>>> 2508392ef0b47bcd0830352cd3e30f3d3b98945e
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        Rquant = np.nanmean(Rquant, axis=0)

    return {'mfiAdjMean1':mfiAdjMean1, 'tnpbsa':tnpbsa, 'kaBruhns':kaBruhns, \
            'meanPerCond1':meanPerCond1, 'mfiAdjMean2':mfiAdjMean2, \
<<<<<<< HEAD
            'meanPerCond2':meanPerCond2, 'Rquant':Rquant, \
            'RquantTups':RquantTups}
=======
            'meanPerCond2':meanPerCond2, 'Rquant':Rquant}
>>>>>>> 2508392ef0b47bcd0830352cd3e30f3d3b98945e
