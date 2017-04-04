import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
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
        self.FcgRs = ['FcgRI', 'FcgRIIB', 'FcgRIII', 'FcgRIV', 'FcgRn', 'TRIM21']
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
        outputLbnd = np.full((6), np.nan)
        outputReq = np.full((6), np.nan)
        outputRbnd = np.full((6), np.nan)
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
            stoneModOut = StoneMod(logR,Ka,v,Kx*Ka,L0, fullOutput = True)
            outputLbnd[k] = stoneModOut[0]
            outputRbnd[k] = stoneModOut[1]
            outputReq[k] = stoneModOut[4]
            outputRmulti[k] = stoneModOut[2]
            outputnXlink[k] = stoneModOut[3]

        return (outputLbnd, outputRbnd, outputRmulti, outputnXlink, outputReq)

    def pdOutputTable(self, z):
        # Takes in a list of shape (8) for z in the format of [logR, logR, logR, logR, logR, logR, kx, v, Li]
        # Organizes the binding prediction between the 24 Ig-FcgR pairs calculated by StoneModMouse(x)
        # Outputs a pandas table of binding prediction
        stoneModMurine = []
        labels = []

        # Set labels for columns of pandas table
        for i in self.FcgRs:
            for j in ['-Lbnd', '-Rbnd', '-Rmulti', '-nXlink', '-Req']:
                labels.append(i+j)

        # Make a 3-d array of StoneModMouse output for each Ig
        for i in range(len(self.Igs)):
            x = z[:]
            x.insert(self.IgIDX, self.Igs[i])
            stoneModMurine.append(np.transpose(self.StoneModMouse(x)))

        # Reshape data for pandas table
        output = np.array(stoneModMurine)

        output = np.reshape(output,(4,30))

        # Make pandas table of binding predictions of Ig-FcgR pairs
        table = pd.DataFrame(np.array(output), index = self.Igs, columns = labels)
        return table

    def pdAvidityTable(self, y, vl, vu):
        # Takes in a list of shape (8) for y <x without avidity v>, lower bond for avidity vl, and upper bond for avidity vu
        # Organizes a pandas table of binding predictions for a given Ig as avidity varies
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

    def NimmerjahnMultiLinear(self, z):
        # Multi-Linear regression of FcgR binding predictions for effectiveness of IgG therapy
        reg = linear_model.LinearRegression()
        tbN = self.NimmerjahnEffectTable(z)
        # Assign independent variables and dependent variable "effect"
        # Current independent variables: FcgRbnd for FcgRI, FcgRIIB, FcgRIII, and FcgRIV
        independent = np.array(tbN.iloc[list(range(2,6)), list(range(1,21,5))].apply(np.log10))
        independent = independent.reshape(4,4)
        effect = np.array(tbN.iloc[list(range(2,6)),30])
        effect = effect.reshape(4,1)
        # Linear regression and plot result
        result = reg.fit(independent, effect)
#        plt.scatter(effect, reg.predict(independent), color='black')
#        plt.plot(effect, reg.predict(independent), color='blue', linewidth=3)
        #plt.show()
        return result

    def NimmerjahnLasso(self, z):
        # Lasso regression of IgG1, IgG2a, and IgG2b effectiveness with binding predictions as potential parameters
        las = linear_model.Lasso(alpha = 0.005, normalize = True)
        tbN = self.NimmerjahnEffectTable(z)
        tbNparam = tbN.iloc[:, list(range(30))]
        tbN_norm = (tbNparam - tbNparam.mean()) / (tbNparam.max() - tbNparam.min())
        # Assign independent variables and dependent variable "effect"
        # Current independent variables: FcgRbnd for FcgRI, FcgRIIB, FcgRIII, and FcgRIV
        independent = np.array(tbN_norm.iloc[list(range(6)), list(range(20))])
        independent = independent.reshape(6,20)
        effect = np.array(tbN.iloc[list(range(6)),30])
        effect = effect.reshape(6,1)
        # Linear regression and plot result
        res = las.fit(independent, effect)
        coe = res.coef_
        coe = coe.reshape(4,5)
#        print(las.score(independent, effect))
#        print(coe)
        plt.scatter(effect, las.predict(independent), color='red')
        plt.plot(effect, las.predict(independent), color='blue', linewidth=3)
        plt.show()
        return independent

    def NimmerjahnLassoCrossVal(self, z, printt = False):
        # Cross-validation fails for all 3 IgG subclasses: IgG1, IgG2a, and IgG2b
        las = linear_model.Lasso(alpha = 0.005, normalize = True)
        tbN = self.NimmerjahnEffectTable(z)
        independent = self.NimmerjahnLasso(z)
        effect = np.array(tbN.iloc[list(range(6)),30])
        effect = effect.reshape(6,1)
        for i in range(3):
            l = list(range(6))
            l.pop(2*i+1)
            l.pop(2*i)
            x_train = independent[l,:]
            y_train = effect[l]
            x_test = independent[[2*i,2*i+1],:]
            y_test = effect[[2*i,2*i+1]]
            res = las.fit(x_train, y_train)

            if printt is True:
                print(las.score(x_test, y_test))

            coe = res.coef_
            coe = coe.reshape(4,5)

            if printt is True:
                print(coe)

        return res

    def FcgRPlots(self, z):
        # Plot effectiveness vs. all FcgR binding parameters
        tbN = self.NimmerjahnEffectTable(z)
        tbNparam = tbN.iloc[:, list(range(30))]
        tbN_norm = (tbNparam - tbNparam.mean()) / (tbNparam.max()- tbNparam.min())
        # Initiate variables
        bndParam = []
        eff = []
        index = []
        # Set up binding and effectiveness parameters column
        for j in range(20):
            bndParam += list(tbN_norm.iloc[list(range(6)),j])
            eff += list(tbN.iloc[list(range(6)),30])

        # Set index for 20 plots
        for k in range(4):
            for l in range(5):
                index.extend([int(str(k+1)+str(l+1))]*6)
        # Plot effectiveness vs. each binding parameter
        plotTb = np.transpose(np.array([index, bndParam, eff]))
        table = pd.DataFrame(plotTb, columns = ['index', 'bndParam', 'eff'])
        sns.lmplot(x="bndParam", y="eff", col = 'index', hue = 'index', col_wrap=2, ci=None, palette="muted", data=table, size = 3)

    def NimmerjahnTb_Knockdown(self, z):
        tbK = self.NimmerjahnEffectTable(z)
        # remove Req columns
        l = list(range(31))
        for i in range(6):
            col = 5*(5-i)+4
            l.pop(col)
        tbK = tbK.iloc[list(range(6)), l]

        # Set up tbK1 for FcgRIIB knockdown, see Figure 3B
        tbK1 = tbK.iloc[:, list(range(24))]
        tbK1.index = funcAppend(tbK1.index, '-FcgRIIB-/-')
        FcgRIIBcol = tbK.columns[4:8]
        l1 = list(range(24))
        for i in range(4):
            l1.pop(7-i)
        tbK1 = tbK1.iloc[:, l1]
        for j in range(4):
            tbK1.insert((4+j), FcgRIIBcol[j], 0)
        tbK1.loc[:,'Effectiveness'] = pd.Series([0,.70,0,1,0,0.75], index=tbK1.index)

        # set up tbK2 for FcgRI knockdown, IgG2a treatment
        tbK2 = tbK.iloc[(2,3), list(range(24))]
        tbK2.index = funcAppend(tbK2.index, '-FcgRI-/-')
        FcgRIcol = tbK.columns[0:4]
        l2 = list(range(24))
        for i in range(4):
            l2.pop(0)
        tbK2 = tbK2.iloc[:, l2]
        for j in range(4):
            tbK2.insert(j, FcgRIcol[j], 0)
        tbK2.loc[:,'Effectiveness'] = pd.Series([0,0.80], index=tbK2.index)

        # set up tbK3 for FcgRIII knockdown, IgG2a treatment
        tbK3 = tbK.iloc[(2,3), list(range(24))]
        tbK3.index = funcAppend(tbK3.index, '-FcgRIII-/-')
        FcgRIIIcol = tbK.columns[8:12]
        l3 = list(range(24))
        for i in range(4):
            l3.pop(11-i)
        tbK3 = tbK3.iloc[:, l3]
        for j in range(4):
            tbK3.insert(8+j, FcgRIIIcol[j], 0)
        tbK3.loc[:,'Effectiveness'] = pd.Series([0,0.93], index=tbK3.index)

        # set up tbK4 table for FcgRI knockdown, FcgRIV blocking, IgG2a treatment
        tbK4 = tbK.iloc[(2,3), list(range(24))]
        tbK4.index = funcAppend(tbK4.index, '-FcgRI,IV-/-')
        FcgRIcol2 = tbK.columns[0:4]
        FcgRIVcol = tbK.columns[12:16]
        l4 = list(range(24))
        for i in range(4):
            l4.pop(15-i)
        for i in range(4):
            l4.pop(3-i)
        tbK4 = tbK4.iloc[:, l4]
        for j in range(4):
            tbK4.insert(j, FcgRIcol2[j], 0)
        for j in range(4):
            tbK4.insert(12+j, FcgRIVcol[j], 0)
        tbK4.loc[:,'Effectiveness'] = pd.Series([0,0.35], index=tbK4.index)

        # Join tbK, tbK1, tbK2, tbK3, and TbK4 into one table
        tbNK = tbK.append([tbK1, tbK2, tbK3, tbK4])

        return tbNK

    def NimmerjahnKnockdownLasso(self, z):
        # Lasso regression of IgG1, IgG2a, and IgG2b effectiveness with binding predictions as potential parameters
        las = linear_model.Lasso(alpha = 0.01, normalize = True)
        tbN = self.NimmerjahnTb_Knockdown(z)
        tbNparam = tbN.iloc[:, list(range(24))]
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())
        # Assign independent variables and dependent variable "effect"
        independent = np.array(tbN_norm.iloc[:, list(range(16))])
        independent = independent.reshape(18,16)
        effect = np.array(tbN.iloc[:,24])
        effect = effect.reshape(18,1)
        # Linear regression and plot result
        res = las.fit(independent, effect)
        coe = res.coef_
        coe = coe.reshape(4,4)
#        print(las.score(independent, effect))
#        print(coe)
        plt.scatter(effect, las.predict(independent), color='red')
        plt.plot(effect, las.predict(independent), color='blue', linewidth=3)
        plt.xlabel("Effectiveness")
        plt.ylabel("Prediction")
        plt.show()
        return res

    def KnockdownLassoCrossVal(self, z, logspace = False, printt = False):
        # Cross validate KnockdownLasso by using a pair of rows as test set
        # Predicts for IgG1, IgG2a, IgG2a-IIB-/-, IgG2b-IIB-/-, IgG2a-I-/-, and IgG2a-I,IV-/-
        # Fails to predict for IgG2b, IgG1-IIB-/-, IgG2a-III-/-
        # In logspace, works for IgG2a, IgG2a-IIB-/-, IgG2b-IIB-/-, and IgG2a-I,IV-/-
        las = linear_model.Lasso(alpha = 0.01, normalize = True)
        tbN = self.NimmerjahnTb_Knockdown(z)
        tbN1 = tbN.copy()
        if logspace is True:
            for i in range (18):
                for j in range(24):
                    if np.isnan(tbN1.iloc[i,j]) is False:
                        if tbN1.iloc[i,j] >= 1:
                            tbN1.ix[i,j] = np.log2(tbN1.iloc[i,j])
                        elif tbN1.iloc[i,j] < 1:
                            tbN1.ix[i,j] = 0
        tbNparam = tbN1.iloc[:, list(range(24))]
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())

        # Iterate over each set of 2 rows being the test set
        for r in range(9):
            ls = list(range(18))
            ls.pop(2*r+1)
            ls.pop(2*r)
            x_train = np.array(tbN_norm.iloc[ls, list(range(16))])
            y_train = np.array(tbN.iloc[ls,24])
            x_test = np.array(tbN_norm.iloc[[2*r,2*r+1], list(range(16))])
            y_test = np.array(tbN.iloc[[2*r,2*r+1],24])
            res = las.fit(x_train, y_train)

            if printt is True:
                print(las.score(x_train,y_train))
                print(las.score(x_test, y_test))
                print(y_test,las.predict(x_test))
#            y1 = y_test[1]
#            y1 = np.array(y1)
#            print(1-abs(las.predict(x_test[1,:])-y1)/y1)
#            plt.scatter(y_train, las.predict(x_train), color='red')
#            plt.scatter(y_test, las.predict(x_test), color='green')
#            plt.plot(y_train, las.predict(x_train), color='blue', linewidth=3)
#            plt.xlabel("Effectiveness")
#            plt.ylabel("Prediction")
#            plt.show()
#            coe = res.coef_
#            coe = coe.reshape(4,4)
#            print(coe)
        return res

    def KnockdownLassoCrossVal2(self, z):
        # Cross validate KnockdownLasso(v=10) by using a row as test set
        # Predictive when test sets are IgG1, IgG2a, IgG1-IIB-/-, IgG2a-IIB-/-, IgG2b-IIB-/-, IgG2a-I-/-, IgG2a-III-/-,
        # Kind of predictive for IgG2b, IgG2a-I,IV-/- (predicted = 2*actual) ()
        las = linear_model.Lasso(alpha = 0.01, normalize = True)
        tbN = self.NimmerjahnTb_Knockdown(z)
        tbNparam = tbN.iloc[:, list(range(24))]
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())
        eff = []
        predict = []
        for r in range(9):
#            print(r)
            l = [2*x+1 for x in range(9)]
            l.pop(r)
            x_train = np.array(tbN_norm.iloc[l,list(range(16))])
            y_train = np.array(tbN.iloc[l,24])
            x_test = np.array(tbN_norm.iloc[[2*r+1], list(range(16))])
            y_test = np.array(tbN.iloc[[2*r+1],24])
            res = las.fit(x_train, y_train)
            eff.append(y_test)
            predict.append(las.predict(x_test))
#            print(las.score(x_train,y_train))
#            print(y_test,las.predict(x_test))
#            if y_test != 0:
#                print(1-abs(las.predict(x_test)-y_test)/y_test)
#            plt.scatter(y_train, las.predict(x_train), color='red')
#            plt.scatter(y_test, las.predict(x_test), color='green')
#            plt.plot((0,1),(0,1), ls="--", c=".3")
#            plt.xlabel("Effectiveness")
#            plt.ylabel("Prediction")
#            plt.show()
#            coe = res.coef_
#            coe = coe.reshape(4,4)
#            print(coe)
        plt.scatter(eff, predict, color='green')
        plt.plot((0,1),(0,1), ls="--", c=".3")
        plt.title("Cross-Validation 2")
        plt.xlabel("Effectiveness")
        plt.ylabel("Prediction")
        plt.show()
        return res

    def KnockdownLassoCrossVal3(self, z):
        # Cross validate KnockdownLasso(v=10) by using a row as test set
        # Predictive when test sets are IgG1, IgG2a, IgG1-IIB-/-, IgG2a-IIB-/-, IgG2b-IIB-/-, IgG2a-I-/-, IgG2a-III-/-,
        # Kind of predictive for IgG2b, IgG2a-I,IV-/- (predicted = 2*actual) ()
        las = linear_model.Lasso(alpha = 0.01, normalize = True)
        tbN = self.NimmerjahnTb_Knockdown(z)
        tbN1 = tbN.copy()
        for i in range (18):
            for j in range(24):
                if np.isnan(tbN1.iloc[i,j]) is False:
                    if tbN1.iloc[i,j] >=1:
                        tbN1.ix[i,j] = np.log2(tbN1.iloc[i,j])
                    elif tbN1.iloc[i,j] < 1:
                        tbN1.ix[i,j] = 0
        tbNparam = tbN1.iloc[:, list(range(24))]
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())
        eff = []
        predict = []
        for r in range(9):
#            print(r)
            l = [2*x+1 for x in range(9)]
            l.pop(r)
            x_train = np.array(tbN_norm.iloc[l,list(range(16))])
            y_train = np.array(tbN.iloc[l,24])
            x_test = np.array(tbN_norm.iloc[[2*r+1], list(range(16))])
            y_test = np.array(tbN.iloc[[2*r+1],24])
            res = las.fit(x_train, y_train)
            eff.append(y_test)
            predict.append(las.predict(x_test))
#            print(las.score(x_train,y_train))
#            print(y_test,las.predict(x_test))
#            if y_test != 0:
#                print(1-abs(las.predict(x_test)-y_test)/y_test)
#            plt.scatter(y_train, las.predict(x_train), color='red')
#            plt.scatter(y_test, las.predict(x_test), color='green')
#            plt.plot((0,1),(0,1), ls="--", c=".3")
#            plt.xlabel("Effectiveness")
#            plt.ylabel("Prediction")
#            plt.show()
#            coe = res.coef_
#            coe = coe.reshape(4,4)
#            print(coe)
        plt.scatter(eff, predict, color='green')
        plt.plot((0,1),(0,1), ls="--", c=".3")
        plt.title("Cross-Validation 3")
        plt.xlabel("Effectiveness")
        plt.ylabel("Prediction")
        plt.show()
        return res

    def KnockdownPCA(self,z):
        # Principle Components Analysis of effectiveness vs. FcgR binding
        # predictions in Knockdown table
        pca = PCA(n_components=5)
        tbN = self.NimmerjahnTb_Knockdown(z)
        tbNparam = tbN.iloc[:, list(range(24))]
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())
        # Assign independent variables and dependent variable "effect"
        independent = np.array(tbN_norm.iloc[:, list(range(16))])
        independent = independent.reshape(18,16)
        effect = np.array(tbN.iloc[:,24])
        effect = effect.reshape(18,1)

        # Plot explained variance ratio
        result = pca.fit(independent, effect)
        ratio = pca.explained_variance_ratio_
        roundratio = [ '%.6f' % j for j in ratio ]
#        print(ratio)
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
        column = tbN_norm.columns[0:16]
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
