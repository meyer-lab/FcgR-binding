from .StoneModel import StoneMod
import numpy as np
import os
import pandas as pd
from scipy.optimize import brentq
from scipy.misc import comb

np.seterr(over = 'raise')

class StoneModelMouse:
    # Takes in a list of shape (9) for x: Rexp for FcgRs and TRIM21 logR, the kind of Ig, avidity Kx, valency uv, Immune Complex Concentration L0
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))

        self.Igs = ['IgG1', 'IgG2a', 'IgG2b', 'IgG3']
        self.FcgRs = ['FcgRI', 'FcgRIIB', 'FcgRIII', 'FcgRIV', 'FcgRn', 'TRIM21']
        # Read in csv file of murine binding affinities
        self.kaMouse = np.genfromtxt(os.path.join(path,'./data/murine-affinities.csv'), delimiter=',', skip_header=1, usecols=list(range(1,5)))
        # Indices for elements in x
        self.IgIDX = 6
        self.kxIDX = 7
        self.uvIDX = 8
        self.L0IDX = 9

    def StoneModMouse(self, x, fullOutput = False):
        ## Returns the number of mutlivalent ligand bound to a cell with 10^logR
        ## receptors, granted each epitope of the ligand binds to the receptor
        ## kind in question with affinity Ka and cross-links with
        ## other receptors with crosslinking constant Kx = 10^logKx. All
        ## equations derived from Stone et al. (2001).

        # Assign Ig type to a number corresponding to the row of Ka
        x1 = x[:]
        for i in range(4):
            if self.Igs[i] == x[self.IgIDX]:
                x1[self.IgIDX] = np.nan
                l = i
#        if type(x[self.IgIDX]) != int:
#            return (np.nan, np.nan, np.nan)
        #print(x[self.IgIDX])

        # Assign inputs for StoneMod
        x1 = np.array(x1)
        v = x1[self.uvIDX]
        Kx = np.power(10, x1[self.kxIDX])
        L0 = x1[self.L0IDX]

        # Initiate numpy arrays for StoneMod outputs
        outputLbnd = np.full((6), np.nan)
        outputReq = np.full((6), np.nan)
        outputRbnd = np.full((6), np.nan)

        if fullOutput:
            outputRmulti = np.full((6), np.nan)
            outputnXlink = np.full((6), np.nan)

        # Iterate over each FcgR
        for k in range(6):
            logR = x1[k]
            ## Set the affinity for the binding of the FcgR and IgG in question
            Ka = self.kaMouse[k][l]
            if Ka == '+' or Ka == 0 or np.isnan(Ka):
                continue
            Ka = float(Ka)
            ## Calculate the MFI which should result from this condition according to the model
            stoneModOut = StoneMod(logR,Ka,v,Kx,L0, fullOutput = True)
            outputLbnd[k] = stoneModOut[0]
            outputRbnd[k] = stoneModOut[1]
            outputReq[k] = stoneModOut[4]

            # Fill in Rmulti and nXlink for full output
            if fullOutput:
                outputRmulti[k] = stoneModOut[2]
                outputnXlink[k] = stoneModOut[3]

        if fullOutput:
            return (outputLbnd, outputRbnd, outputRmulti, outputnXlink, outputReq)
        return (outputLbnd, outputRbnd, outputReq)

    def pdOutputTable(self, x, fullOutput = False):
        # Organizes the binding prediction between the 24 Ig-FcgR pairs calculated by StoneModMouse(x)
        # Outputs a pandas table of binding prediction
        stoneModMurine = []
        labels = []

        # Set labels for columns of pandas table
        if fullOutput:
            for i in self.FcgRs:
                for j in ['-Lbnd', '-Rbnd', '-Rmulti', '-nXlink', '-Req']:
                    labels.append(i+j)
        else:
            for i in self.FcgRs:
                for j in ['-Lbnd', '-Rbnd', '-Req']:
                    labels.append(i+j)

        # Make a 3-d array of StoneModMouse output for each Ig
        if fullOutput:
            for i in range(len(self.Igs)):
                x[self.IgIDX] = self.Igs[i]
                stoneModMurine.append(np.transpose(self.StoneModMouse(x, fullOutput = True)))
        else:
            for i in range(len(self.Igs)):
                x[self.IgIDX] = self.Igs[i]
                stoneModMurine.append(np.transpose(self.StoneModMouse(x)))

        # Reshape data for pandas table
        output = np.array(stoneModMurine)
        if fullOutput:
            output = np.reshape(output,(4,30))
        else:
            output = np.reshape(output,(4,18))

        # Make pandas table of binding predictions of Ig-FcgR pairs
        table = pd.DataFrame(np.array(output), index = self.Igs, columns = labels)
        return table

    def pdAvidityTable(self, x, vl, vu, fullOutput = False):
        # Takes in a list of shape (9) for x, lower bond for avidity vl, and upper bond for avidity vu
        # Organizes a pandas table of binding predictions for a given Ig as avidity varies
        tb1 = pd.DataFrame()
        Ig = x[self.IgIDX]
        idx = []
        # Concatenating a pandas table for a range of avidity
        if fullOutput == False:
            for i in range(vl, vu+1):
                x[self.uvIDX] = i
                tb = self.pdOutputTable(x, fullOutput = False)
                tb1 = pd.concat([tb1, tb.loc[[Ig]]])
        elif fullOutput == True:
            for j in range(vl, vu+1):
                x[self.uvIDX] = j
                tb = self.pdOutputTable(x, fullOutput = True)
                tb1 = pd.concat([tb1, tb.loc[[Ig]]])
        # Indexing
        for k in range(vl, vu+1):
            idx.append(Ig+'-'+str(k))
        tb1.index = idx
        return tb1

    def NimmerjahnEffectTable(self, x):
        x1 = x[:]
        tbN = pd.DataFrame()
        idx = []
        tv = self.pdOutputTable(x, fullOutput = True)
        x1[self.uvIDX] = 1
        t1 = self.pdOutputTable(x1, fullOutput = True)
        for i in self.Igs:
            for j in [1, x[self.uvIDX]]:
                if j == 1:
                    tbN = pd.concat([tbN, t1.loc[[i]]])
                else:
                    tbN = pd.concat([tbN, tv.loc[[i]]])
                idx.append(i+'-'+str(j))
        tbN.index = idx
        tbN.loc[:,'Effectiveness'] = pd.Series([0,0,0,0.95,0,0.20,0,0], index=tbN.index)
        return tbN

#    def NimmerjahnMultiLinear(self, x):
#        tbN = self.NimmerjahnEffectTable(x)
