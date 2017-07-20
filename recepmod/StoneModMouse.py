import pandas as pd
import numpy as np


np.seterr(over='raise')


def funcAppend(indexList, nameApp):
    idx = []
    for i in indexList:
        idx.append(i + nameApp)
    return idx


class StoneModelMouse:
    # Takes in a list of shape (9) for x: Rexp for FcgRs logR, the kind of Ig,
    # avidity Kx, valency uv, Immune Complex Concentration L0
    def __init__(self):
        import os
        from .StoneHelper import getMedianKx

        path = os.path.dirname(os.path.abspath(__file__))

        self.Igs = ['IgG1', 'IgG2a', 'IgG2b', 'IgG3']
        self.FcgRs = ['FcgRI', 'FcgRIIB', 'FcgRIII', 'FcgRIV']
        # Read in csv file of murine binding affinities
        self.kaM = np.genfromtxt(os.path.join(path, './data/murine-affinities.csv'),
                                 delimiter=',',
                                 skip_header=1,
                                 usecols=list(range(1, 6)),
                                 dtype=np.float64)

        self.kaMouse = self.kaM[:, list(range(4))]
        self.kaIgG2b_Fucose = self.kaM[:, 4].reshape(4, 1)
        self.L0 = 1E-9
        self.v = 4
        self.Kx = getMedianKx()
        self.logR = np.full((len(self.FcgRs),), np.log10(10**5), dtype=np.float64)

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
                # Set the affinity for the binding of the FcgR and IgG in question
                Ka = self.kaMouse[k][l]

                # Calculate the MFI which should result from this condition according to the model
                stoneModOut = StoneMod(self.logR[k], Ka, self.v,
                                       self.Kx * Ka, self.L0, fullOutput=True)
                output[l, :, k] = np.asarray(stoneModOut, dtype=np.float)

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
            labels.append(p[0] + p[1])

        # Make a 3-d array of StoneModMouse output for each Ig
        stoneModMurine = self.StoneModMouse()

        # Reshape data for pandas table
        output = np.reshape(stoneModMurine, (4, -1), order='F')

        # Make pandas table of binding predictions of Ig-FcgR pairs
        return pd.DataFrame(output, index=self.Igs, columns=labels)

    def pdAvidityTable(self):
        """
        Organizes a pandas table of binding predictions for a given Ig as avidity varies from 1 to v
        """
        tb1 = pd.DataFrame()
        idx = []
        # Concatenating a pandas table for a range of avidity
        for j in range(1, self.v + 1):
            self.v = j
            tb = self.pdOutputTable()
            tb1 = pd.concat([tb1, tb])

            for _, Ig in enumerate(self.Igs):
                idx.append(Ig + '-' + str(j))

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
            idx[i] = idx[i] + '-' + str(self.v)
            idx[i + len(self.Igs)] = idx[i + len(self.Igs)] + '-1'
        tbN.index = idx

        tbN = tbN.sort_index()

        # Append effectiveness data on the 31 column
        tbN.loc[:, 'Effectiveness'] = pd.Series([0, 0, 0, 0.95, 0, 0.20, 0, 0], index=tbN.index)

        return tbN

    def NimmerjahnEffectTableAffinities(self):
        # Setup initial table
        tbK = pd.DataFrame(np.transpose(self.kaMouse),
                           index=self.Igs,
                           columns=self.FcgRs)
        tbK.loc[:, 'Effectiveness'] = pd.Series([0, 0.95, 0.20, 0], index=tbK.index)

        # Set up tbK1 for FcgRIIB knockdown, see Figure 3B
        tbK1 = tbK.copy()
        tbK1.index = funcAppend(tbK1.index, '-FcgRIIB-/-')
        tbK1.loc[:, 'Effectiveness'] = pd.Series([0.7, 1, 0.75, 0],
                                                 index=tbK1.index)
        tbK1.iloc[:, 1] = 0.0

        # set up tbK2 for FcgRI, FcgRIII, FcgRI/IV knockdown, IgG2a treatment
        tbK2 = tbK.iloc[[1, 1, 1], :].copy()
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
        tbK3 = pd.DataFrame(np.transpose(self.kaIgG2b_Fucose), index=[
                            'IgG2b-Fucose-/-'], columns=self.FcgRs)
        tbK3.loc[:, 'Effectiveness'] = pd.Series([0.70], index=tbK3.index)

        # Join tbK, tbK1, tbK2 into one table
        return tbK.append([tbK1, tbK2, tbK3])

    def IgG2b_Fucose(self):
        from .StoneModel import StoneMod

        output = np.full((2, len(self.FcgRs), 4), np.nan)
        v = [1, self.v]
        for k in range(len(self.FcgRs)):
            for i in range(2):
                Ka = self.kaIgG2b_Fucose[k]
                stoneModOut = np.asarray(
                    StoneMod(self.logR[k], Ka, v[i], self.Kx * Ka, self.L0, fullOutput=True))
                output[i, k, :] = stoneModOut[:4]
        return output.reshape(2, 16)

    def tabWrite(self, filename, matrix, names):
        tnl = '\\tabularnewline'

        f = open(filename, 'w')
        f.write(
            '\\section{Supplement}\\label{supplement}\n\n\\begin{longtable}[]{@{}rrrrrr@{}}\n\\toprule\n')
        for ii, name in enumerate(names):
            f.write(name)
            if ii != 5:
                f.write(' & ')
        f.write(tnl + '\n\\midrule\n\\endhead\n')
        for row in matrix:
            for ii, item in enumerate(row):
                f.write('{\centering ' + str(item) + '}')
                if ii != 5:
                    f.write(' & ')
            f.write(tnl + '\n')
        f.write('\n\\bottomrule\n\\end{longtable}\n')

    def writeModelData(self, filename):
        import pytablewriter as ptw

        tbN = self.NimmerjahnEffectTableAffinities()
        tbN.insert(0, 'Condition', tbN.index)

        def rename(name):
            name = 'mFcγRI' if name == 'FcgRI' else name
            name = 'mFcγRIIB' if name == 'FcgRIIB' else name
            name = 'mFcγRIII' if name == 'FcgRIII' else name
            name = 'mFcγRIV' if name == 'FcgRIV' else name
            return name

        def renameList(names):
            return [rename(name) for name in names]

        def matrixScientific(matrix):
            for j in range(matrix.shape[0]):
                for k in range(matrix.shape[1]):
                    if not isinstance(matrix[j, k], str):
                        if matrix[j, k] > 1:
                            matrix[j, k] = sci(matrix[j, k])
                        else:
                            matrix[j, k] = r'$' + str(matrix[j, k]) + '$'
            return matrix

        def sciSeries(series):
            return [sci(val) for val in series]

        def sci(val):
            if isinstance(val, str):
                return val
            elif val == 0:
                return r'$$0.0$$'
            else:
                try:
                    logval = np.log10(val)
                    if int(logval) == '0':
                        return r'$$' + str(val / (10**np.floor(logval)))[0:3] + \
                               '$$'
                    else:
                        return r'$$' + str(val / (10**np.floor(logval)))[0:3] + \
                           '*10^' + str(int(logval)) + '$$'
                except OverflowError:
                    return r'$$0.0$$'

        def renameIgg(name):
            name = 'm'+name
            name = 'mIgG1-FcγRIIB-/-' if name == 'mIgG1-FcgRIIB-/-' else name
            name = 'mIgG2a-FcγRIIB-/-' if name == 'mIgG2a-FcgRIIB-/-' else name
            name = 'mIgG2b-FcγRIIB-/-' if name == 'mIgG2b-FcgRIIB-/-' else name
            name = 'mIgG3-FcγRIIB-/-' if name == 'mIgG3-FcgRIIB-/-' else name
            name = 'mIgG2a-FcγRI-/-' if name == 'mIgG2a-FcgRI-/-' else name
            name = 'mIgG2a-FcγRIII-/-' if name == 'mIgG2a-FcgRIII-/-' else name
            name = 'mIgG2a-FcγRI,IV-/-' if name == 'mIgG2a-FcgRI,IV-/-' else name
            name = 'mIgG2b-Fucose-/-' if name == 'mIgG2b-Fucose-/-' else name
            return name
            

        def sciSeries(series):
            return [sci(val) for val in series]

        ## Rename columns of DataFrame 
        tbN.columns = renameList(tbN.columns)
        tbN = tbN.apply(sciSeries)

        writer = ptw.MarkdownTableWriter()
        writer.from_dataframe(tbN)

        ## Change writer stream to filename
        with open(filename, 'w') as f:
            writer.stream = f
            writer.write_table()

        writer.close()

    def KnockdownPCA(self):
        """ Principle Components Analysis of FcgR-IgG affinities. """
        from sklearn.decomposition import PCA

        pca = PCA(n_components=4)

        X = self.NimmerjahnEffectTableAffinities().drop('Effectiveness', axis=1)

        scores = pd.DataFrame(pca.fit_transform(X), index=X.index,
                              columns=['PC1', 'PC2', 'PC3', 'PC4'])

        return (scores, pca.explained_variance_ratio_)
