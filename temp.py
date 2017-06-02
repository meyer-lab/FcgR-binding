import os
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from recepmod.figures.FigureCommon import Legend

mur = pd.read_csv('recepmod/data/pca-murine.csv', index_col=0)
hum = pd.read_csv('recepmod/data/pca-human.csv', index_col=0)

##mur.plot()
##plt.show()

mur[(mur.IgID == 0) & (mur.avidity == 1)].drop(['avidity', 'ligand', 'IgID'], axis=1).plot()
plt.show()

print(hum)

pcamur = PCA(4)
pcahum = pcamur
Xmur = mur.drop(['avidity', 'ligand', 'IgID'], axis=1)
Xmur = pcamur.fit_transform(StandardScaler().fit_transform(Xmur))
##print(Xmur)
