from .StoneModel import StoneMod
import numpy as np
import os
import pandas as pd
from scipy.optimize import brentq
from scipy.misc import comb
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks")

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
            if Ka == '+' or np.isnan(Ka):
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
        # Initiate variables
        x1 = x[:]
        tbN = pd.DataFrame()
        idx = []
        # create pandas tables
        tv = self.pdOutputTable(x, fullOutput = True)
        x1[self.uvIDX] = 1
        t1 = self.pdOutputTable(x1, fullOutput = True)
        # Compose a table of shape (8,30), 2 rows for each IgG
        for i in self.Igs:
            for j in [1, x[self.uvIDX]]:
                if j == 1:
                    tbN = pd.concat([tbN, t1.loc[[i]]])
                else:
                    tbN = pd.concat([tbN, tv.loc[[i]]])
                idx.append(i+'-'+str(j))
        tbN.index = idx
        # Append effectiveness data on the 31 column
        tbN.loc[:,'Effectiveness'] = pd.Series([0,0,0,0.95,0,0.20,0,0], index=tbN.index)
        return tbN

    def NimmerjahnMultiLinear(self, x, fullOutput = True):
        # Multi-Linear regression of FcgR binding predictions for effectiveness of IgG therapy
        reg = linear_model.LinearRegression()
        tbN = self.NimmerjahnEffectTable(x)
        # Assign independent variables and dependent variable "effect"
        # Current independent variables: FcgRbnd for FcgRI, FcgRIIB, FcgRIII, and FcgRIV
        independent = np.array(tbN.iloc[list(range(2,6)), list(range(1,21,5))].apply(np.log10))
        independent = independent.reshape(4,4)
        effect = np.array(tbN.iloc[list(range(2,6)),30])
        effect = effect.reshape(4,1)
        # Linear regression and plot result
        result = reg.fit(independent, effect)

        return result

    def NimmerjahnLasso(self, x, fullOutput = True):
        # Lasso regression of IgG1, IgG2a, and IgG2b effectiveness with binding predictions as potential parameters
        las = linear_model.Lasso(alpha = 0.005, normalize = True)
        tbN = self.NimmerjahnEffectTable(x)
        # Assign independent variables and dependent variable "effect"
        # Current independent variables: FcgRbnd for FcgRI, FcgRIIB, FcgRIII, and FcgRIV
        independent = np.array(tbN.iloc[list(range(6)), list(range(20))])
        independent = independent.reshape(6,20)
        effect = np.array(tbN.iloc[list(range(6)),30])
        effect = effect.reshape(6,1)
        # Linear regression and plot result
        res = las.fit(independent, effect)
        coe = res.coef_
        coe = coe.reshape(4,5)
        print(las.score(independent, effect))
        print(coe)
        plt.scatter(effect, las.predict(independent), color='red')
        plt.plot(effect, las.predict(independent), color='blue', linewidth=3)
        plt.show()
        return res

    def FcgRPlots(self, x):
        # Plot effectiveness vs. all FcgR binding parameters
        tbN = self.NimmerjahnEffectTable(x)
        tbNparam = tbN.iloc[:, list(range(30))]
        tbN_norm = (tbNparam - tbNparam.mean()) / (tbNparam.max() - tbNparam.min())
        # Initiate variables
        bndParam = []
        eff = []
        # Set up binding parameters column
        for j in range(20):
            bndParam += list(tbN_norm.iloc[list(range(6)),j])
        # Set up effectiveness column
        for i in range(20):
            eff += list(tbN.iloc[list(range(6)),30])
        index = []
        # Set index for 20 plots
        for k in range(4):
            for l in range(5):
                for n in range(6):
                    index.append(int(str(k+1)+str(l+1)))
        # Plot effectiveness vs. each binding parameter
        plotTb = np.array([index, bndParam, eff])
        plotTb = np.transpose(plotTb)
        table = pd.DataFrame(plotTb, columns = ['index', 'bndParam', 'eff'])
        sns.lmplot(x="bndParam", y="eff", col = 'index', hue = 'index', col_wrap=2, ci=None, palette="muted", data=table, size = 3)
