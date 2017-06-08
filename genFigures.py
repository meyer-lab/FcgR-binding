#!/usr/bin/env python3

import sys
import matplotlib
matplotlib.use('AGG')
import svgutils.transform as st
import multiprocessing
from recepmod.figures.FigureCommon import figList
from recepmod.StoneModMouse import StoneModelMouse

parallel = True

fdir = './Manuscript/Figures/'


def runFunc(nameOut):
    """ Run the code for a particular figure. """
    try:
        import matplotlib
        matplotlib.use('AGG')
        import warnings
        warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
        exec('from recepmod.figures import ' + nameOut)
        ff = eval(nameOut + '.makeFigure()')
        ff.savefig(fdir + nameOut + '.svg', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
        print(nameOut + ' is done.')
        return None
    except Exception as e:
        return e


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        # Just build one figure.
        nameOut = 'Figure' + sys.argv[1]

        a = runFunc(nameOut)

        if isinstance(a, Exception):
            raise a

    else:
        if parallel is True:
            pool = multiprocessing.Pool()
            result = pool.map_async(runFunc, figList)
        else:
            list(map(runFunc, figList))

        # Output data table
        StoneModelMouse().writeModelData('./Manuscript/Text/07_ModelData.md')

        # IF we're running in parallel we need to wait for Figure 2 to finish
        # Close the pool
        if parallel is True:
            pool.close()
            pool.join()

            for i in result.get():
                if isinstance(i, Exception):
                    raise i

        # Overlay Figure 2 cartoon
        template = st.fromfile(fdir + 'Figure2.svg')
        cartoon = st.fromfile('./recepmod/figures/Figure2_model_diagram.svg').getroot()

        cartoon.moveto(10, -15)

        template.append(cartoon)
        template.save(fdir + 'Figure2.svg')

        # Overlay Figure 3 cartoon
        template = st.fromfile(fdir + 'Figure3.svg')
        cartoon = st.fromfile('./recepmod/figures/Figure3_model_diagram.svg').getroot()

        cartoon.moveto(173, 160, scale=0.16)

        template.append(cartoon)
        template.save(fdir + 'Figure3.svg')

        # Overlay Figure 4 cartoon
        template = st.fromfile(fdir + 'Figure4.svg')
        cartoon = st.fromfile('./recepmod/figures/Figure4_regression_approach.svg').getroot()

        cartoon.moveto(10, 20, scale=0.66)

        template.append(cartoon)
        template.save(fdir + 'Figure4.svg')
