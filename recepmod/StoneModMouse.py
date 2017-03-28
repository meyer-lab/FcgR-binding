import os
import pandas as pd
import numpy as np
from scipy.misc import comb
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn import tree
import matplotlib.pyplot as plt
import seaborn as sns
import pydotplus
from .StoneModel import StoneMod
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
#        if type(x[self.IgIDX]) != int:
#            return (np.nan, np.nan, np.nan)
        #print(x[self.IgIDX])

        # Assign inputs for StoneMod
        x1 = np.array(x1)
        v = x1[self.uvIDX]
        Kx = x1[self.kxIDX]
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

    def pdOutputTable(self, z, fullOutput = False):
        # Takes in a list of shape (8) for z in the format of [logR, logR, logR, logR, logR, logR, kx, v, Li]
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
                x = z[:]
                x.insert(self.IgIDX, self.Igs[i])
                stoneModMurine.append(np.transpose(self.StoneModMouse(x, fullOutput = True)))
        else:
            for i in range(len(self.Igs)):
                x = z[:]
                x.insert(self.IgIDX, self.Igs[i])
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

    def pdAvidityTable(self, y, vl, vu, fullOutput = False):
        # Takes in a list of shape (8) for y <x without avidity v>, lower bond for avidity vl, and upper bond for avidity vu
        # Organizes a pandas table of binding predictions for a given Ig as avidity varies
        tb1 = pd.DataFrame()
        Ig = y[self.IgIDX]
        idx = []
        # Concatenating a pandas table for a range of avidity
        if fullOutput is False:
            for i in range(vl, vu+1):
                x = y[:]
                x.insert(self.uvIDX, i)
                x.pop(self.IgIDX)
                z = x
                tb = self.pdOutputTable(z, fullOutput = False)
                tb1 = pd.concat([tb1, tb.loc[[Ig]]])
        elif fullOutput is True:
            for j in range(vl, vu+1):
                x = y[:]
                x.insert(self.uvIDX, j)
                x.pop(self.IgIDX)
                z = x
                tb = self.pdOutputTable(z, fullOutput = True)
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
        tv = self.pdOutputTable(z, fullOutput = True)
        z1[self.uvIDX-1] = 1
        t1 = self.pdOutputTable(z1, fullOutput = True)
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

    def NimmerjahnMultiLinear(self, z, fullOutput = True):
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

    def NimmerjahnLassoCrossVal(self, z):
        las = linear_model.Lasso(alpha = 0.005, normalize = True)
        tbN = self.NimmerjahnEffectTable(z)
        independent = self.NimmerjahnLasso(z)
        effect = np.array(tbN.iloc[list(range(6)),30])
        effect = effect.reshape(6,1)
        x_train, x_test, y_train, y_test = train_test_split(independent, effect, test_size=1/6, random_state=0)
        res = las.fit(x_train, y_train)
#        print(las.score(x_test, y_test))
        coe = res.coef_
        coe = coe.reshape(4,5)
#        print(coe)
        return res

    def FcgRPlots(self, z):
        # Plot effectiveness vs. all FcgR binding parameters
        tbN = self.NimmerjahnEffectTable(z)
        tbNparam = tbN.iloc[:, list(range(30))]
        tbN_norm = (tbNparam - tbNparam.mean()) / (tbNparam.max()- tbNparam.min())
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

    def Rmulti_v(self, kx, ka, L0, logR0, v):
        # Returns the number of receptors bond at or above each avidity
        # Initiate variables
        R0 = np.power(10,logR0)
        sigma = 0.001
        Req = R0/2
        high = R0
        low = 0
        L_bound = 0
        L = []
        Rmultiv = []
        while abs(R0 - Req*(1 + v*L0*ka*(1+kx*Req)**(v-1))) > sigma:
            if (R0 - Req*(1 + v*L0*ka*(1+kx*Req)**(v-1))) > 0:
                low = Req
            elif (R0 - Req*(1 + v*L0*ka*(1+kx*Req)**(v-1))) < 0:
                high = Req
            Req = (high+low)/2
        for i in range(1, int(v+1)):
            L.append(comb(v,i)*(kx**(i-1))*L0*ka*(Req**i))
            L_bound += L[i-1]
        R = L[:]
        for j in range(len(L)):
            R[j] = R[j]*(j+1)
        for k in range(len(R)):
            Rmultiv.append(sum(R[k:len(R)]))
        Rmultiv = np.array(Rmultiv)
        return Rmultiv

    def RmultiAvidity(self, x):
        # Assign Ig type to a number corresponding to the row of Ka
        x1 = x[:]
        for i in range(4):
            if self.Igs[i] == x[self.IgIDX]:
                x1[self.IgIDX] = np.nan
                l = i

        # Assign inputs for Rmulti_v
        x1 = np.array(x1)
        v = int(x1[self.uvIDX])
        Kx = x1[self.kxIDX]
        L0 = x1[self.L0IDX]

        # Initiate numpy arrays for StoneMod outputs
        outputRmultiv = np.full((6,v), np.nan)

        # Iterate over each FcgR
        for k in range(6):
            logR = x1[k]
            ## Set the affinity for the binding of the FcgR and IgG in question
            Ka = self.kaMouse[k][l]
            if Ka == '+' or np.isnan(Ka):
                continue
            Ka = float(Ka)
            ## Calculate the MFI which should result from this condition according to the model
            RmultivOut = self.Rmulti_v(Kx, Ka, L0, logR, v)
            outputRmultiv[k] = RmultivOut
        outputRmultiv = outputRmultiv.reshape(6,int(v))
        return outputRmultiv

    def RmultiAvidityTable(self,z):
        # Organizes the binding prediction between the 24 Ig-FcgR pairs calculated by StoneModMouse(x)
        # Outputs a pandas table of binding prediction
        v = z[self.uvIDX-1]
        Rmultiv = []
        labels = []

        # Set labels for columns of pandas table
        for i in self.FcgRs:
            for j in range(v):
                labels.append(i+'-'+str(j+1))

        # Make a 3-d array of StoneModMouse output for each Ig
        for i in range(len(self.Igs)):
            x = z[:]
            x.insert(self.IgIDX, self.Igs[i])
            Rmultiv.append(self.RmultiAvidity(x))

        # Reshape data for pandas table
        output = np.array(Rmultiv)
        output = np.reshape(output,(4,6*v))

        # Make pandas table of binding predictions of Ig-FcgR pairs
        tbv = pd.DataFrame(np.array(output), index = self.Igs, columns = labels)
        # Append effectiveness data on the last column
        tbv.loc[:,'Effectiveness'] = pd.Series([0,0.95,0.20,0], index=tbv.index)
        return tbv

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
        idx1 = []
        for i in tbK1.index:
            idx1.append(i+'-FcgRIIB-/-')
        tbK1.index = idx1
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
        idx2 = []
        for i in tbK2.index:
            idx2.append(i+'-FcgRI-/-')
        tbK2.index = idx2
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
        idx3 = []
        for i in tbK3.index:
            idx3.append(i+'-FcgRIII-/-')
        tbK3.index = idx3
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
        idx4 = []
        for i in tbK4.index:
            idx4.append(i+'-FcgRI,IV-/-')
        tbK4.index = idx4
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
        tbNK = tbK.append(tbK1)
        tbNK = tbNK.append(tbK2)
        tbNK = tbNK.append(tbK3)
        tbNK = tbNK.append(tbK4)

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
        return independent

    def KnockdownLassoCrossVal(self, z):
        # Cross validate KnockdownLasso by using a pair of rows as test set
        # Predicts for IgG1, IgG2a, IgG2a-IIB-/-, IgG2b-IIB-/-, IgG2a-I-/-, and IgG2a-I,IV-/-
        # Fails to predict for IgG2b, IgG1-IIB-/-, IgG2a-III-/-
        las = linear_model.Lasso(alpha = 0.008, normalize = True)
        tbN = self.NimmerjahnTb_Knockdown(z)
        independent = self.NimmerjahnKnockdownLasso(z)
        for r in range(9):
#            print(r)
            ls = list(range(18))
            ls.pop(2*r+1)
            ls.pop(2*r)
            x_train = independent[ls,:]
            y_train = np.array(tbN.iloc[ls,24])
            x_test = independent[[2*r,2*r+1],:]
            #x_test.reshape(2,16)
            y_test = np.array(tbN.iloc[[2*r,2*r+1],24])
            #y_test.reshape(2,1)
            res = las.fit(x_train, y_train)
#            print(las.score(x_train,y_train))
#            print(las.score(x_test, y_test))
#            print(y_test,las.predict(x_test))
            y1 = y_test[1]
            y1 = np.array(y1)
#            print(1-abs(las.predict(x_test[1,:])-y1)/y1)
#            plt.scatter(y_train, las.predict(x_train), color='red')
#            plt.scatter(y_test, las.predict(x_test), color='green')
#            plt.plot(y_train, las.predict(x_train), color='blue', linewidth=3)
#            plt.xlabel("Effectiveness")
#            plt.ylabel("Prediction")
#            plt.show()
            coe = res.coef_
            coe = coe.reshape(4,4)
#            print(coe)
        return res

    def KnockdownLassoCrossVal2(self, z):
        # Cross validate KnockdownLasso(v=10) by using a row as test set
        # Predictive when test sets are IgG1, IgG2a, IgG1-IIB-/-, IgG2a-IIB-/-, IgG2b-IIB-/-, IgG2a-I-/-, IgG2a-III-/-, 
        # Kind of predictive for IgG2b, IgG2a-I,IV-/-
        las = linear_model.Lasso(alpha = 0.008, normalize = True)
        tbN = self.NimmerjahnTb_Knockdown(z)
        independent = self.NimmerjahnKnockdownLasso(z)
        for r in range(9):
#            print(r)
            l = [2*x+1 for x in range(9)]
            l.pop(r)
            x_train = independent[l,:]
            y_train = np.array(tbN.iloc[l,24])
            x_test = independent[[2*r+1],:]
            y_test = np.array(tbN.iloc[[2*r+1],24])
            res = las.fit(x_train, y_train)
#            print(las.score(x_train,y_train))
#            print(y_test,las.predict(x_test))
#            if y_test != 0:
#                print(1-abs(las.predict(x_test)-y_test)/y_test)
#            plt.scatter(y_train, las.predict(x_train), color='red')
#            plt.scatter(y_test, las.predict(x_test), color='green')
#            plt.plot(y_train, las.predict(x_train), color='blue', linewidth=3)
#            plt.xlabel("Effectiveness")
#            plt.ylabel("Prediction")
#            plt.show()
            coe = res.coef_
            coe = coe.reshape(4,4)
#            print(coe)
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
        print(pca.explained_variance_ratio_)
        plt.figure(1, figsize=(4, 3))
        plt.clf()
        plt.axes([.2, .2, .7, .7])
        plt.plot(pca.explained_variance_, linewidth=2)
        plt.axis('tight')
        plt.xlabel('n_components')
        plt.ylabel('explained_variance_')
        plt.show()

        # Plot loading
        trans = PCA(n_components=2).fit_transform(independent, effect)
        plt.scatter(trans[:, 0], trans[:, 1], color='red')
        #plt.plot(trans[:, 0], trans[:, 1], color='blue', linewidth=3)
        plt.title("First 2 PCA directions")
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.show()
#        print(trans)
        return result

    def DecisionTree(self,z):
        # Decision Tree using Knockdown table with a pair of rows corresponding
        # to same IgG and FcgRconditions taken out.
        # Does not accurately predict for IgG2b, IgG1-IIB-/-, IgG2b-IIB-/-, and IgG2a-I-/-
        tbN = self.NimmerjahnTb_Knockdown(z)
        tbNparam = tbN.iloc[:, list(range(24))]
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())
        independent = np.array(tbN_norm.iloc[:, list(range(16))])
        independent = independent.reshape(18,16)
        effect = np.array(tbN.iloc[:,24])
        effect = effect.reshape(18,1)
        for i in range(18):
            if effect[i] >= 0.5:
                effect[i] = 1
            else:
                effect[i] = 0
        #effect = np.array([0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0]
        # Assign independent variables and dependent variable "effect"

        for i in range(9):
            ls = list(range(18))
            ls.pop(2*i+1)
            ls.pop(2*i)
            independent1 = np.array(independent[ls,:])
            effect1 = np.array(effect[ls])
        # Construct Decision Tree
            clf = tree.DecisionTreeClassifier()
            clf = clf.fit(independent1, effect1)
#            print(clf.predict(independent[[2*i,2*i+1], :]))
#            print(clf.predict_proba(independent[[2*i,2*i+1], :]))
#        dot_data = tree.export_graphviz(clf, out_file=None)
#        graph = pydotplus.graph_from_dot_data(dot_data)
#        graph.write_pdf("DecisionTree.pdf")
        return effect

    def DecisionTree2(self,z):
        # Decision Tree with one row removed
        # Fails to predict for IgG2b, IgGI-IIB-/-, IgG2b-IIB-/-, IgG2a-FcgRI-/-
        tbN = self.NimmerjahnTb_Knockdown(z)
        tbNparam = tbN.iloc[:, list(range(24))]
        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())
        independent = np.array(tbN_norm.iloc[:, list(range(16))])
        independent = independent.reshape(18,16)
        effect = np.array(tbN.iloc[:,24])
        effect = effect.reshape(18,1)
        for i in range(18):
            if effect[i] >= 0.5:
                effect[i] = 1
            else:
                effect[i] = 0
        #effect = np.array([0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0]
        # Assign independent variables and dependent variable "effect"

        for i in range(18):
            ls = list(range(18))
            ls.pop(i)
            independent1 = np.array(independent[ls,:])
            effect1 = np.array(effect[ls])
        # Construct Decision Tree
            clf = tree.DecisionTreeClassifier()
            clf = clf.fit(independent1, effect1)
#            print(clf.predict(independent[i:i+1, :]))
#            print(clf.predict_proba(independent[i:i+1, :]))
        return effect
    
#    def RmultivKnockdownTb(self, z):
#        
#        
#    def LassoRmultiv(self,z):
#        # Lasso regression of Rmultiv
#        las = linear_model.Lasso(alpha = 0.01, normalize = True)
#        tbN = self.RmultiAvidityTable(z)
#        tbNparam = tbN.iloc[:, list(range(24))]
#        tbN_norm = (tbNparam - tbNparam.min()) / (tbNparam.max() - tbNparam.min())
#        # Assign independent variables and dependent variable "effect"
#        independent = np.array(tbN_norm.iloc[:, list(range(16))])
#        independent = independent.reshape(18,16)
#        effect = np.array(tbN.iloc[:,24])
#        effect = effect.reshape(18,1)
#        # Linear regression and plot result
#        res = las.fit(independent, effect)
#        coe = res.coef_
#        coe = coe.reshape(4,4)
##        print(las.score(independent, effect))
##        print(coe)
#        plt.scatter(effect, las.predict(independent), color='red')
#        plt.plot(effect, las.predict(independent), color='blue', linewidth=3)
#        plt.xlabel("Effectiveness")
#        plt.ylabel("Prediction")
#        plt.show()
#        return independent
#    
#    def CrossValRmultiv(self,z):
#        
#    def PCARmultiv(self,z):
#        
#    def TreeRmultiv(self,z):
#        
#    def OrtizTable(self,z):
        