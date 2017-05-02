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
        exec('from recepmod.figures import ' + nameOut)
        ff = eval(nameOut + '.makeFigure()')
        ff.savefig(fdir + nameOut + '.svg', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
        ff.savefig(fdir + nameOut + '.pdf', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
        print(nameOut)
    except Exception as e:
        return e


if __name__ == '__main__':

    if parallel is True:
        pool = multiprocessing.Pool()
        result = pool.map_async(runFunc, figList)
    else:
        list(map(runFunc, figList))

    # Output data table
    StoneModelMouse().writeModelData(fdir + 'ModelData.md')

    # IF we're running in parallel we need to wait for Figure 2 to finish
    # Close the pool
    if parallel is True:
        pool.close()
        pool.join()

        for i in result.get():
            if isinstance(i, Exception):
                raise i

    # Overlay cartoon
    template = st.fromfile(fdir + 'Figure2.svg')
    cartoon = st.fromfile('./recepmod/figures/Figure2_model_diagram.svg').getroot()

    cartoon.moveto(10, -15)

    template.append(cartoon)
    template.save(fdir + 'Figure2.svg')
