import numpy as np
import pandas as pd
from tqdm import tqdm
from recepmod.StoneModMouseFit import InVivoPredict
from concurrent.futures import ProcessPoolExecutor

# Make an array of the expression levels to use
expr = np.linspace(0, 4, num=6)

# Make expression levels into a grid
a = np.meshgrid(expr, expr, expr, expr)

# Reshape this into an actual grid
e = np.concatenate((np.reshape(a[0], (-1, 1)),
                    np.reshape(a[1], (-1, 1)),
                    np.reshape(a[2], (-1, 1)),
                    np.reshape(a[3], (-1, 1))), axis=1)

# Create the output vector
outt = np.zeros((e.shape[0], 1), dtype=np.float)

# Split into list
elist = np.split(e, e.shape[0])


def F(exprVV):
    return InVivoPredict(exprV=np.squeeze(exprVV), cPred=False)[0]


pool = ProcessPoolExecutor()

ii = 0

for f in tqdm(pool.map(F, elist), total=len(outt), smoothing=0):
    outt = f
    ii += 1

df = pd.DataFrame(e)
df['pref'] = outt

df.to_csv('output.csv')
