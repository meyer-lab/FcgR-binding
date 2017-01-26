##import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from StoneHelper import *

x = np.arange(200)
plt.plot(x,x)
plt.show()

seaborn_colorblindSteal()
##Colors = sns.color_palette('colorblind')
##print(type(Colors[1][1]))
