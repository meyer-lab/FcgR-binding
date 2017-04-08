import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product
import re
sns.set(style="ticks")

np.seterr(over = 'raise')

def funcAppend(indexList, nameApp):
    idx = []
    for i in indexList:
        idx.append(i+nameApp)
    return idx

class StoneModelMouse:
    # Takes in a list of shape (9) for x: Rexp for FcgRs and TRIM21 logR, the kind of Ig, avidity Kx, valency uv, Immune Complex Concentration L0
    def __init__(self):
        import os

        path = os.path.dirname(os.path.abspath(__file__))

        self.Igs = ['IgG1', 'IgG2a', 'IgG2b', 'IgG3']
        self.FcgRs = ['FcgRI', 'FcgRIIB', 'FcgRIII', 'FcgRIV']
        # Read in csv file of murine binding affinities
        self.kaMouse = np.genfromtxt(os.path.join(path,'./data/murine-affinities.csv'), delimiter=',', skip_header=1, usecols=list(range(1,5)))
        # Indices for elements in x
        self.IgIDX = 6
        self.kxIDX = 7
        self.uvIDX = 8
        self.L0IDX = 9

    def StoneModMouse(self, x):
        '''
        Returns the number of mutlivalent ligand bound to a cell with 10^logR
        receptors, granted each epitope of the ligand binds to the receptor
        kind in question with affinity Ka and cross-links with
        other receptors with crosslinking constant Kx = 10^logKx. All
        equations derived from Stone et al. (2001).
        '''

        from .StoneModel import StoneMod

        # Assign Ig type to a number corresponding to the row of Ka
        x1 = x[:]
        for i in range(4):
            if self.Igs[i] == x[self.IgIDX]:
                x1[self.IgIDX] = np.nan
                l = i

        # Assign inputs for StoneMod
        x1 = np.array(x1)
        v = x1[self.uvIDX]
        Kx = x1[self.kxIDX]
        L0 = x1[self.L0IDX]

        # Initiate numpy arrays for StoneMod outputs
        output = np.full((5, len(self.FcgRs)), np.nan)

        # Iterate over each FcgR
        for k in range(len(self.FcgRs)):
            logR = x1[k]
            ## Set the affinity for the binding of the FcgR and IgG in question
            Ka = float(self.kaMouse[k][l])

            ## Calculate the MFI which should result from this condition according to the model
            stoneModOut = StoneMod(logR,Ka,v,Kx*Ka,L0, fullOutput = True)
            output[:, k] = np.asarray(stoneModOut, dtype = np.float)

        return output

    def pdOutputTable(self, z):
        """
        Takes in a list of shape (8) for z in the format of [logR, logR, logR,
        logR, logR, logR, kx, v, Li] Organizes the binding prediction between
        the 24 Ig-FcgR pairs calculated by StoneModMouse(x). Outputs a pandas
        table of binding prediction
        """

        stoneModMurine = []
        labels = []

        # Set labels for columns of pandas table
        for p in product(self.FcgRs, ['-Lbnd', '-Rbnd', '-Rmulti', '-nXlink', '-Req']):
            labels.append(p[0]+p[1])

        # Make a 3-d array of StoneModMouse output for each Ig
        for i in range(len(self.Igs)):
            x = z[:]
            x.insert(self.IgIDX, self.Igs[i])
            stoneModMurine.append(np.transpose(self.StoneModMouse(x)))

        # Reshape data for pandas table
        output = np.reshape(np.array(stoneModMurine), (4, -1))

        # Make pandas table of binding predictions of Ig-FcgR pairs
        return pd.DataFrame(np.array(output), index=self.Igs, columns=labels)

    def pdAvidityTable(self, y, vl, vu):
        """
        Takes in a list of shape (8) for y <x without avidity v>, lower bond
        for avidity vl, and upper bond for avidity vu. Organizes a pandas table
        of binding predictions for a given Ig as avidity varies
        """
        tb1 = pd.DataFrame()
        Ig = y[self.IgIDX]
        idx = []
        # Concatenating a pandas table for a range of avidity
        for j in range(vl, vu+1):
            x = y[:]
            x.insert(self.uvIDX, j)
            x.pop(self.IgIDX)
            z = x
            tb = self.pdOutputTable(z)
            tb1 = pd.concat([tb1, tb.loc[[Ig]]])
        # Indexing
        for k in range(vl, vu+1):
            idx.append(Ig+'-'+str(k))
        tb1.index = idx
        return tb1

    def NimmerjahnEffectTable(self, z):
        # Makes a pandas dataframe of shape(8,31) with 2 different avidities for each 1gG
        # Initiate variables
        z1 = z[:]
        tbN = pd.DataFrame()
        idx = []
        # create pandas tables
        tv = self.pdOutputTable(z)
        z1[self.uvIDX-1] = 1
        t1 = self.pdOutputTable(z1)
        # Compose a table of shape (8,30), 2 rows for each IgG
        for i in self.Igs:
            for j in [1, z[self.uvIDX-1]]:
                if j == 1:
                    tbN = pd.concat([tbN, t1.loc[[i]]])
                else:
                    tbN = pd.concat([tbN, tv.loc[[i]]])
                idx.append(i+'-'+str(j))
        tbN.index = idx
        # Append effectiveness data on the 31 column
        tbN.loc[:,'Effectiveness'] = pd.Series([0,0,0,0.95,0,0.20,0,0], index=tbN.index)
        return tbN

    def FcgRPlots(self, z):
        # TODO: Fix
        # Plot effectiveness vs. all FcgR binding parameters
        tbN = self.NimmerjahnEffectTable(z)
        tbNparam = tbN.iloc[:, list(range(30))]
        tbN_norm = (tbNparam - tbNparam.mean()) / (tbNparam.max()- tbNparam.min())
        # Initiate variables
        bndParam = []
        eff = list(tbN.iloc[list(range(6)),30]) * 20
        index = []
        # Set up binding and effectiveness parameters column
        for j in range(20):
            bndParam += list(tbN_norm.iloc[list(range(6)),j])

        # Set index for 20 plots
        for k in product(range(1,5), range(1,6)):
            index.extend([int(str(k[0])+str(k[1]))]*6)

        # Plot effectiveness vs. each binding parameter
        plotTb = np.transpose(np.array([index, bndParam, eff]))
        table = pd.DataFrame(plotTb, columns = ['index', 'bndParam', 'eff'])
        sns.lmplot(x="bndParam",
                   y="eff",
                   col = 'index',
                   hue = 'index',
                   col_wrap=2,
                   ci=None,
                   palette="muted",
                   data=table,
                   size = 3)
        plt.show()

    def NimmerjahnTb_Knockdown(self, z):
        tbK = self.NimmerjahnEffectTable(z)
        # remove Req columns
        tbK = tbK.select(lambda x: not re.search('Req', x), axis=1)

        # Set up tbK1 for FcgRIIB knockdown, see Figure 3B
        tbK1 = tbK.copy()
        tbK1.index = funcAppend(tbK1.index, '-FcgRIIB-/-')
        tbK1.loc[:,'Effectiveness'] = pd.Series([0, 0.7, 0, 1, 0, 0.75, 0, 0],
                                                index=tbK1.index)
        tbK1.iloc[:, 4:8] = 0.0

        # set up tbK2 for FcgRI knockdown, IgG2a treatment
        tbK2 = tbK.iloc[(2, 3), :].copy()
        tbK2.index = funcAppend(tbK2.index, '-FcgRI-/-')
        tbK2.loc[:,'Effectiveness'] = pd.Series([0, 0.8], index=tbK2.index)
        tbK2.iloc[:, 0:4] = 0.0

        # set up tbK3 for FcgRIII knockdown, IgG2a treatment
        tbK3 = tbK.iloc[(2, 3), :].copy()
        tbK3.index = funcAppend(tbK3.index, '-FcgRIII-/-')
        tbK3.loc[:,'Effectiveness'] = pd.Series([0, 0.93], index=tbK3.index)
        tbK3.iloc[:, 8:12] = 0.0

        # set up tbK4 table for FcgRI knockdown, FcgRIV blocking, IgG2a treatment
        tbK4 = tbK.iloc[(2, 3), :].copy()
        tbK4.index = funcAppend(tbK4.index, '-FcgRI,IV-/-')
        tbK4.loc[:,'Effectiveness'] = pd.Series([0, 0.35], index=tbK4.index)
        tbK4.iloc[:, 0:4] = 0.0
        tbK4.iloc[:, 12:16] = 0.0

        # Join tbK, tbK1, tbK2, tbK3, and TbK4 into one table
        return tbK.append([tbK1, tbK2, tbK3, tbK4])

    def NimmerjahnKnockdownLasso(self, z):
        # Lasso regression of IgG1, IgG2a, and IgG2b effectiveness with binding predictions as potential parameters
        las = linear_model.Lasso(alpha = 0.01, normalize = True)

        # Collect data
        independent, effect, tbN = self.modelPrep(z)

        # Linear regression and plot result
        res = las.fit(independent, effect)
        coe = res.coef_
        coe = np.array(coe)
        coetb = pd.DataFrame(coe.reshape(1,16), index = ["coefficient"], columns = tbN.columns[0:16])
        coetb.plot(kind='bar', title = 'Lasso Coefficients')
        plt.show()

        plt.scatter(effect, las.predict(independent), color='red')
        plt.plot(effect, las.predict(independent), color='blue', linewidth=3)
        plt.xlabel("Effectiveness")
        plt.ylabel("Prediction")
        plt.show()
        return res

    def KnockdownLassoCrossVal(self, z, logspace = False, addavidity1 = False):
        """ Cross validate KnockdownLasso by using a pair of rows as test set """
        las = linear_model.Lasso(alpha = 0.01, normalize = True)

        # Collect data
        independent, effect, tbN = self.modelPrep(z, logspace)

        # Iterate over each set of 2 rows being the test set
        eff = []
        predict = []
        for r in range(9):
            if addavidity1 is False:
                l = [2*x+1 for x in range(9)]
                l.pop(r)
                testl = [2*r+1]
            else:
                l = list(range(18))
                l.pop(2*r+1)
                l.pop(2*r)
                testl = [2*r, 2*r+1]
            res = las.fit(independent[l,:], effect[l])

            # Append results from this leave out step
            eff.append(effect[testl])
            predict.append(las.predict(independent[testl,:]))

        plt.scatter(eff, predict, color='green')
        plt.plot((0,1),(0,1), ls="--", c=".3")
        plt.title("Cross-Validation 1")
        plt.xlabel("Effectiveness")
        plt.ylabel("Prediction")
        plt.show()
        return res

    def modelPrep(self, z, logspace = False):
        """ Collect the data and split into X and Y blocks. """
        tbN = self.NimmerjahnTb_Knockdown(z)
        tbNparam = tbN.select(lambda x: not re.search('Effectiveness', x), axis=1)
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())

        # Log transform if needed
        if logspace is True:
            tbNparam = tbNparam.apply(np.log2).replace(-np.inf, -3)

        # Assign independent variables and dependent variable "effect"
        independent = np.array(tbN_norm)
        effect = np.array(tbN['Effectiveness'])

        return (independent, effect, tbN)

    def KnockdownPCA(self,z):
        """
        Principle Components Analysis of effectiveness vs. FcgR binding
        predictions in Knockdown table
        """
        pca = PCA(n_components=5)

        # Collect data
        independent, effect, tbN = self.modelPrep(z)

        # Plot explained variance ratio
        result = pca.fit(independent, effect)
        ratio = pca.explained_variance_ratio_
        roundratio = [ '%.6f' % j for j in ratio ]

        plt.figure(1, figsize=(4, 3))
        plt.clf()
        plt.axes([.2, .2, .7, .7])
        plt.plot(pca.explained_variance_, linewidth=2)
        plt.axis('tight')
        plt.xlabel('n_components')
        plt.ylabel('explained_variance_')
        plt.show()
        # Heatmap with first 5 eigenvectors
        scores = pca.components_.reshape(5,16)
        idx = []
        for i in range(5):
            idx.append("PC"+str(i+1)+'('+str(roundratio[i])+')')
        column = tbN.columns[0:16]
        PCscoretb = pd.DataFrame(scores, index=idx, columns=column)
        sns.heatmap(PCscoretb)
        plt.title("PCA heatmap")
        plt.show()

        # Plot loading
        trans = PCA(n_components=2).fit_transform(independent, effect)
#        print(trans.reshape(6,6))
        plt.scatter(trans[:, 0], trans[:, 1], color='red')
#        plt.plot(trans[:, 0], trans[:, 1], color='blue', linewidth=3)
        plt.title("First 2 PCA directions")
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.show()
#        print(trans)
        return result
