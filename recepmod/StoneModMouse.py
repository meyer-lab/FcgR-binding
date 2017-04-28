import re
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import explained_variance_score
import seaborn as sns
from .StoneModel import StoneMod

sns.set(style="ticks")

np.seterr(over = 'raise')

def funcAppend(indexList, nameApp):
    idx = []
    for i in indexList:
        idx.append(i+nameApp)
    return idx

class StoneModelMouse:
    # Takes in a list of shape (9) for x: Rexp for FcgRs logR, the kind of Ig, avidity Kx, valency uv, Immune Complex Concentration L0
    def __init__(self):
        import os
        from .StoneHelper import getMedianKx

        path = os.path.dirname(os.path.abspath(__file__))

        self.Igs = ['IgG1', 'IgG2a', 'IgG2b', 'IgG3']
        self.FcgRs = ['FcgRI', 'FcgRIIB', 'FcgRIII', 'FcgRIV']
        # Read in csv file of murine binding affinities
        self.kaM = np.genfromtxt(os.path.join(path,'./data/murine-affinities.csv'), 
                                     delimiter=',', 
                                     skip_header=1, 
                                     usecols=list(range(1,6)),
                                     dtype=np.float64)

        self.kaMouse = self.kaM[:, list(range(4))]
        self.kaIgG2b_Fucose = self.kaM[:, 4].reshape(4,1)
        self.L0 = 1E-9
        self.v = 4
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
        from itertools import product

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
            self.v = j
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
        tbK1.iloc[:, 1] = 0.0

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
        
        # set up IgG2b, -Fucose
        tbK3 = pd.DataFrame(np.transpose(self.kaIgG2b_Fucose), index = ['IgG2b-Fucose-'], columns = self.FcgRs)
        tbK3.loc[:,'Effectiveness'] = pd.Series([0.70], index=tbK3.index)

        # Join tbK, tbK1, tbK2 into one table
        return tbK.append([tbK1, tbK2, tbK3])

    def NimmerjahnPredictByAffinities(self):
        """ This will run ordinary linear regression using just affinities of receptors. """
        from sklearn import linear_model
        from sklearn.model_selection import cross_val_predict

        # Run ridge regression with forced direction or simple OLS
        lr = linear_model.LinearRegression()

        data = self.NimmerjahnEffectTableAffinities()
        data['ActMax'] = data.apply(lambda x: max(x.FcgRI, x.FcgRIII, x.FcgRIV), axis=1)

        X = data[['ActMax', 'FcgRIIB']]
        y = data['Effectiveness']

        # Log transform to keep ratios
        X = X.apply(np.log2).replace(-np.inf, -3)

        # Run crossvalidation predictions at the same time
        predicted = cross_val_predict(lr, X, y, cv=X.shape[0])

        # How well did we do on crossvalidation?
        crossval_perf = explained_variance_score(y, predicted)

        # Do direct regression too
        lr.fit(X, y)

        # How well did we do on direct?
        direct_perf = explained_variance_score(y, lr.predict(X))

        data['DirectPredict'] = lr.predict(X)
        data['CrossPredict'] = predicted

        return (direct_perf, crossval_perf, data)

    def IgG2b_Fucose(self):
        output = np.full((2, len(self.FcgRs), 4), np.nan)
        v = [1, self.v]
        for k in range(len(self.FcgRs)):
            for i in range(2):
                Ka = self.kaIgG2b_Fucose[k]
                stoneModOut = np.asarray(StoneMod(self.logR[k],Ka,v[i],self.Kx*Ka,self.L0, fullOutput = True), dtype = np.float)
                output[i, k, :] = stoneModOut[:4]
        return output.reshape(2,16)

    def NimmerjahnTb_Knockdown(self):
        tbK = self.NimmerjahnEffectTable()
        IgG2b_fucose = self.IgG2b_Fucose()
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

        # set up tbK5 for IgG2b-Fucose-/-
        # Add effectiveness
        IgG2b_fucose = np.insert(IgG2b_fucose, 16, [0, 0.70], axis=1)
        tbK5idx = funcAppend(tbK.index[4:6], '-Fucose-/-')
        tbK5 = pd.DataFrame(IgG2b_fucose, index = tbK5idx, columns = tbK.columns)

        # Join tbK, tbK1, tbK2, tbK3, and TbK4 into one table
        return tbK.append([tbK1, tbK2, tbK3, tbK4, tbK5])

    def writeModelData(self, filename, logspace=False, addavidity1=False):
        import pytablewriter

        # Collect data
        _, _, tbN = self.modelPrep(logspace, addavidity1)

        writer = pytablewriter.MarkdownTableWriter()

        writer.from_dataframe(tbN)

        # change output stream to a file
        with open(filename, 'w') as f:
            writer.stream = f
            writer.write_table()

        writer.close()

    def InVivoPredict(self, logspace=False, addavidity1=True):
        """ Cross validate KnockdownLasso by using a pair of rows as test set """
        from sklearn.cross_decomposition import PLSRegression
        from sklearn.model_selection import cross_val_predict, LeaveOneOut, LeaveOneGroupOut
        from .StoneHelper import rep

        las = PLSRegression(n_components=3, scale=False)
        scale = StandardScaler()

        # Collect data
        X, y, tbN = self.modelPrep(logspace, addavidity1)

        X = scale.fit_transform(X)

        # Setup the crossvalidation iterators
        if addavidity1 is False:
            loo = LeaveOneOut()
            looI = loo.split(X, y)
        else:
            loo = LeaveOneGroupOut()
            looI = loo.split(X, y, groups = rep(range(12), 2))

        # Run crossvalidation
        predict = cross_val_predict(las, X, y, cv = looI)

        # How well did we do on crossvalidation?
        crossval_perf = explained_variance_score(y, predict)

        # Do direct regression too
        las.fit(X, y)

        # How well did we do on direct?
        direct_perf = explained_variance_score(y, las.predict(X))

        print("Performance of the plsr in vivo model on crossval: " + str(crossval_perf))

        tbN['DirectPredict'] = las.predict(X)
        tbN['CrossPredict'] = predict

        return (direct_perf, crossval_perf, tbN, las, scale)

    def modelPrep(self, logspace, addavidity1):
        """ Collect the data and split into X and Y blocks. """
        tbN = self.NimmerjahnTb_Knockdown()

        if addavidity1 is False:
            temp = tbN.apply(lambda x: int(x.name.split('-')[1]), axis=1)
            tbN = tbN.loc[temp > 1, :]

        # Assign independent variables and dependent variable
        X = tbN.drop('Effectiveness', axis=1)

        # Log transform if needed
        if logspace is True:
            X = X.apply(np.log2).replace(-np.inf, -5)

        y = tbN['Effectiveness'].as_matrix()

        return (X.as_matrix(), y, tbN)

    def PCA(self, plott = False):
        """ Principle Components Analysis of FcgR binding predictions """
        from sklearn.decomposition import PCA

        pca = PCA(n_components=5)
        table = self.pdAvidityTable()

        # remove Req columns
        table = table.select(lambda x: not re.search('Req', x), axis=1)

        X = StandardScaler().fit_transform(np.array(table))

        # Fit PCA
        result = pca.fit_transform(X)

        # Assemble scores
        scores = pd.DataFrame(result, index=table.index, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'])
        scores['Avidity'] = scores.apply(lambda x: int(x.name.split('-')[1]), axis=1)
        scores['Ig'] = scores.apply(lambda x: x.name.split('-')[0], axis=1)

        return (scores, pca.explained_variance_ratio_)

    def KnockdownPCA(self, logspace = False, addavidity1 = True):
        from sklearn.decomposition import PCA
        pca = PCA(n_components=5)
        scale = StandardScaler()
        X, y, tbN = self.modelPrep(logspace, addavidity1)
        X = scale.fit_transform(X)
        result = pca.fit_transform(X, y)
        scores = pd.DataFrame(result, index=tbN.index, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'])
        scores['Avidity'] = scores.apply(lambda x: int(x.name.split('-')[1]), axis=1)
        scores['Ig'] = scores.apply(lambda x: x.name.split('-')[0], axis=1)
        knockdown = []
        for i in tbN.index:
            string = i.split('-')[0]+'-'+i.split('-')[1]
            i = i.replace(string, '')
            if i == '':
                knockdown.append('None')
            else:
                knockdown.append(i[1:])
        scores['Knockdown'] = knockdown
        return (scores, pca.explained_variance_ratio_)


def MultiAvidityPredict(M, las, scale):
    """ Make predictions for the effect of avidity and class. """
    table = M.pdAvidityTable().select(lambda x: not re.search('Req', x), axis=1)

    table['Predict'] = las.predict(scale.transform(table))
    table['Avidity'] = table.apply(lambda x: int(x.name.split('-')[1]), axis=1)
    table['Ig'] = table.apply(lambda x: x.name.split('-')[0], axis=1)

    return table
