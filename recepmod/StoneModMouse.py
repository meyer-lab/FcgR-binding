import re
from itertools import product
import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.model_selection import cross_val_predict, LeaveOneOut, LeaveOneGroupOut
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from .StoneHelper import rep, getMedianKx
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
        self.kaMouse = np.genfromtxt(os.path.join(path,'./data/murine-affinities.csv'), 
                                     delimiter=',', 
                                     skip_header=1, 
                                     usecols=list(range(1,5)),
                                     dtype=np.float64)
        self.L0 = 1E-9
        self.v = 10
        self.Kx = getMedianKx()
        self.logR = np.full((len(self.FcgRs),), np.log10(10**5), dtype = np.float64)

    def StoneModMouse(self):
        '''
        Returns the number of mutlivalent ligand bound to a cell with 10^logR
        receptors, granted each epitope of the ligand binds to the receptor
        kind in question with affinity Ka and cross-links with
        other receptors with crosslinking constant Kx = 10^logKx. All
        equations derived from Stone et al. (2001).
        '''
        from .StoneModel import StoneMod

        # Initiate numpy arrays for StoneMod outputs
        output = np.full((len(self.Igs), 5, len(self.FcgRs)), np.nan)

        # Iterate over each FcgR
        for l in range(len(self.Igs)):
            for k in range(len(self.FcgRs)):
                ## Set the affinity for the binding of the FcgR and IgG in question
                Ka = self.kaMouse[k][l]

                ## Calculate the MFI which should result from this condition according to the model
                stoneModOut = StoneMod(self.logR[k],Ka,self.v,self.Kx*Ka,self.L0, fullOutput = True)
                output[l, :, k] = np.asarray(stoneModOut, dtype = np.float)

        return output

    def pdOutputTable(self):
        """
        Takes in a list of shape (8) for z in the format of [logR, logR, logR,
        logR, logR, logR, kx, v, Li] Organizes the binding prediction between
        the 24 Ig-FcgR pairs calculated by StoneModMouse(x). Outputs a pandas
        table of binding prediction
        """

        # Set labels for columns of pandas table
        labels = []
        for p in product(self.FcgRs, ['-Lbnd', '-Rbnd', '-Rmulti', '-nXlink', '-Req']):
            labels.append(p[0]+p[1])

        # Make a 3-d array of StoneModMouse output for each Ig
        stoneModMurine = self.StoneModMouse()

        # Reshape data for pandas table
        output = np.reshape(stoneModMurine, (4, -1), order = 'F')

        # Make pandas table of binding predictions of Ig-FcgR pairs
        return pd.DataFrame(output, index=self.Igs, columns=labels)

    def pdAvidityTable(self):
        """
        Organizes a pandas table of binding predictions for a given Ig as avidity varies from 1 to v
        """
        tb1 = pd.DataFrame()
        idx = []
        # Concatenating a pandas table for a range of avidity
        for j in range(1, self.v+1):
            v = j
            tb = self.pdOutputTable()
            tb1 = pd.concat([tb1, tb])

            for _, Ig in enumerate(self.Igs):
                idx.append(Ig+'-'+str(j))
            
        tb1.index = idx
        return tb1
        
    def NimmerjahnEffectTable(self):
        # Makes a pandas dataframe of shape(8,31) with 2 different avidities for each 1gG
        # Initiate variables
        idx = []
        # create pandas tables
        tv = self.pdOutputTable()
        uv = self.v
        self.v = 1
        tbN = pd.concat([tv, self.pdOutputTable()])
        self.v = uv

        # Redo the row indeces
        idx = list(tbN.index)
        for i in range(len(self.Igs)):
            idx[i] = idx[i]+'-'+str(self.v)
            idx[i+len(self.Igs)] = idx[i+len(self.Igs)]+'-1'
        tbN.index = idx

        tbN = tbN.sort_index()

        # Append effectiveness data on the 31 column
        tbN.loc[:,'Effectiveness'] = pd.Series([0,0,0,0.95,0,0.20,0,0], index=tbN.index)

        return tbN

    def NimmerjahnEffectTableAffinities(self):
        # Setup initial table
        tbK = pd.DataFrame(np.transpose(self.kaMouse),
                           index = self.Igs,
                           columns = self.FcgRs)
        tbK.loc[:,'Effectiveness'] = pd.Series([0, 0.95, 0.20, 0], index=tbK.index)



        # Set up tbK1 for FcgRIIB knockdown, see Figure 3B
        tbK1 = tbK.copy()
        tbK1.index = funcAppend(tbK1.index, '-FcgRIIB-/-')
        tbK1.loc[:,'Effectiveness'] = pd.Series([0.7, 1, 0.75, 0],
                                                index=tbK1.index)
        tbK1.iloc[:, 4:8] = 0.0

        # set up tbK2 for FcgRI, FcgRIII, FcgRI/IV knockdown, IgG2a treatment
        tbK2 = tbK.iloc[(1, 1, 1), :].copy()
        idx = list(tbK2.index)
        idx[0] = idx[0] + '-FcgRI-/-'
        idx[1] = idx[1] + '-FcgRIII-/-'
        idx[2] = idx[2] + '-FcgRI,IV-/-'
        tbK2.index = idx
        tbK2.loc[:, 'Effectiveness'] = pd.Series([0.8, 0.93, 0.35], index=tbK2.index)
        tbK2.iloc[0, 0] = 0.0
        tbK2.iloc[1, 2] = 0.0
        tbK2.iloc[2, 0] = 0.0
        tbK2.iloc[2, 3] = 0.0

        # Join tbK, tbK1, tbK2 into one table
        return tbK.append([tbK1, tbK2])

    def NimmerjahnPredictByAffinities(self, fixed=False, simple=False, logspace=False):
        """ This will run ordinary linear regression using just affinities of receptors. """

        # Run ridge regression with forced direction or simple OLS
        if simple is True:
            lr = linear_model.LinearRegression()
        else:
            lr = linear_model.ElasticNet(positive=fixed, max_iter=10000)

        data = self.NimmerjahnEffectTableAffinities()

        # Log transform if needed
        if logspace is True:
            data = data.apply(np.log2).replace(-np.inf, -5)

        X = data.iloc[:, 0:4]
        y = data['Effectiveness']

        # If we're fixing the parameters, we need to make the inhibitory receptor negative
        if fixed is True:
            X.loc[:, 1] = -X.iloc[:, 1]

        # Run crossvalidation predictions at the same time
        predicted = cross_val_predict(lr, X, y, cv=11)

        # How well did we do on crossvalidation?
        crossval_perf = sklearn.metrics.explained_variance_score(y, predicted)

        # Do direct regression too
        lr.fit(X, y)

        # How well did we do on direct?
        direct_perf = sklearn.metrics.explained_variance_score(y, lr.predict(X))

        data['DirectPredict'] = lr.predict(X)
        data['CrossPredict'] = predicted

        return (direct_perf, crossval_perf, data)

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

    def NimmerjahnTb_Knockdown(self):
        tbK = self.NimmerjahnEffectTable()
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

    def NimmerjahnKnockdownLasso(self, plott=False):
        # Lasso regression of IgG1, IgG2a, and IgG2b effectiveness with binding predictions as potential parameters
        las = linear_model.ElasticNetCV(l1_ratio=0.9, max_iter=100000)

        # Collect data
        independent, effect, tbN = self.modelPrep()

        # Linear regression and plot result
        res = las.fit(independent, effect)
        coe = res.coef_
        coe = np.array(coe)
        coetb = pd.DataFrame(coe.reshape(1,16), index = ["coefficient"], columns = tbN.columns[0:16])

        if plott is True:
            coetb.plot(kind='bar', title = 'Lasso Coefficients')
            plt.show()

        if plott is True:
            plt.scatter(effect, las.predict(independent), color='red')
            plt.plot(effect, las.predict(independent), color='blue', linewidth=3)
            plt.xlabel("Effectiveness")
            plt.ylabel("Prediction")
            plt.show()

        return res

    def KnockdownLassoCrossVal(self, logspace=False, addavidity1=False, plott=False, printt=False):
        """ Cross validate KnockdownLasso by using a pair of rows as test set """
        las = linear_model.ElasticNetCV(l1_ratio=0.9, max_iter=100000)

        # Collect data
        X, y, _ = self.modelPrep(logspace)

        # Setup the crossvalidation iterators
        if addavidity1 is False:
            loo = LeaveOneOut()
            looI = loo.split(X, y)
        else:
            loo = LeaveOneGroupOut()
            looI = loo.split(X, y, groups = rep(range(11), 2))

        # Run crossvalidation
        predict = cross_val_predict(las, X, y, cv = looI, n_jobs=-1)

        # How well did we do on crossvalidation?
        crossval_perf = sklearn.metrics.explained_variance_score(y, predict)

        # Do direct regression too
        las.fit(X, y)

        # How well did we do on direct?
        direct_perf = sklearn.metrics.explained_variance_score(y, las.predict(X))

        if plott is True:
            plt.scatter(effect, predict, color='green')
            plt.plot((0, 1), (0, 1), ls="--", c=".3")
            plt.title("Cross-Validation 1")
            plt.xlabel("Effectiveness")
            plt.ylabel("Prediction")
            plt.show()

        if printt is True:
            print("Performance of the enet in vivo model on crossval: " + str(crossval_perf))

        return (crossval_perf, direct_perf)

    def modelPrep(self, logspace=False):
        """ Collect the data and split into X and Y blocks. """
        tbN = self.NimmerjahnTb_Knockdown()
        tbNparam = tbN.select(lambda x: not re.search('Effectiveness', x), axis=1)
        # Log transform if needed
        if logspace is True:
            tbNparam = tbNparam.apply(np.log2).replace(-np.inf, -5)
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())

        # Assign independent variables and dependent variable "effect"
        independent = np.array(tbN_norm)
        effect = np.array(tbN['Effectiveness'])

        return (independent, effect, tbN)

    def KnockdownPCA(self, plott=False):
        """
        Principle Components Analysis of effectiveness vs. FcgR binding
        predictions in Knockdown table
        """
        pca = PCA(n_components=5)

        # Collect data
        independent, effect, tbN = self.modelPrep()

        # Plot explained variance ratio
        result = pca.fit(independent, effect)
        ratio = pca.explained_variance_ratio_
        roundratio = [ '%.6f' % j for j in ratio ]

        if plott is True:
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

        if plott is True:
            sns.heatmap(PCscoretb)
            plt.title("PCA heatmap")
            plt.show()

        # Plot loading
        trans = PCA(n_components=2).fit_transform(independent, effect)
        
        if plott is True:
            plt.scatter(trans[:, 0], trans[:, 1], color='red')
            plt.title("First 2 PCA directions")
            plt.xlabel("PC1")
            plt.ylabel("PC2")
            plt.show()

        return result

def MultiAvidityPredict(M, paramV):
    """ Make predictions for the effect of avidity and class. """
    table = M.pdAvidityTable()

    # remove Req columns
    table = table.select(lambda x: not re.search('Req', x), axis=1)

    if len(paramV) != (table.shape[1] + 1):
        raise ValueError('Weighting list doesn\'t match data.')

    def transF(inVal):
        return np.dot(paramV[1::], inVal.values) + paramV[0]

    def extractAvidity(inVal):
        return int(inVal.name.split('-')[1])

    def extractIg(inVal):
        return inVal.name.split('-')[0]

    table['Predict'] = table.apply(transF, axis=1)
    table['Avidity'] = table.apply(extractAvidity, axis=1)
    table['Ig'] = table.apply(extractIg, axis=1)

    return table

    
