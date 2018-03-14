#!/usr/bin/env python3

import sys
import matplotlib
matplotlib.use('AGG')
from recepmod.figures.FigureCommon import overlayCartoon

fdir = './Manuscript/Figures/'


if __name__ == '__main__':
    nameOut = 'Figure' + sys.argv[1]

    exec('from recepmod.figures import ' + nameOut)
    ff = eval(nameOut + '.makeFigure()')
    ff.savefig(fdir + nameOut + '.svg', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)

    if sys.argv[1] == '2':
        # Overlay Figure 2 cartoon
        overlayCartoon(fdir + 'Figure2.svg',
                       './recepmod/figures/Figure2_model_diagram.svg', 10, -15)

    elif sys.argv[1] == '3':
        # Overlay Figure 3 cartoon
        overlayCartoon(fdir + 'Figure3.svg',
                       './recepmod/figures/Figure3_model_diagram.svg', 173, 160, 0.16)

    elif sys.argv[1] == '4':
        # Overlay Figure 4 cartoon
        overlayCartoon(fdir + 'Figure4.svg',
                       './recepmod/figures/Figure4_regression_approach.svg', 6, 30, 0.022)

    print(nameOut + ' is done.')
