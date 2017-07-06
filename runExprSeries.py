import numpy as np
from tqdm import trange
from recepmod.StoneModMouseFit import InVivoPredict

# Make an array of the expression levels to use
expr = np.linspace(-2, 3, num=2)

# Make expression levels into a grid
a = np.meshgrid(expr, expr, expr, expr)

# Reshape this into an actual grid
e = np.concatenate((np.reshape(a[0], (-1, 1)),
                    np.reshape(a[1], (-1, 1)),
                    np.reshape(a[2], (-1, 1)),
                    np.reshape(a[3], (-1, 1))), axis=1)

# Create the output vector
outt = np.zeros((e.shape[0], 1), dtype=np.float)

for ii in trange(e.shape[0]):
    outt[ii] = InVivoPredict(exprV=e[ii, :])[0]

print(outt)
