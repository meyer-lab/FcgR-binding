from recepmod.figures.Figure5 import PCAhuman
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd

f = plt.figure()
gs = GridSpec(2,1)
axx = []
for j in range(2):
    axx.append(f.add_subplot(gs[j]))
table = PCAhuman(axx)
cols = table.columns
cutcols = cols[2:-1]

table2 = pd.pivot_table(table,values='RbndPred',index=['Ig'],columns=['FcgR'])
