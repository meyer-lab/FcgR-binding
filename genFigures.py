import matplotlib
matplotlib.use('AGG')
import svgutils.transform as st
import multiprocessing
from recepmod.figures.FigureCommon import figList
from recepmod.StoneModMouse import StoneModelMouse

parallel = True

def runFunc(nameOut):
	print('Starting on ' + nameOut)
	exec('from recepmod.figures import ' + nameOut)
	ff = eval(nameOut + '.makeFigure()')
	ff.savefig('./Manuscript/Figures/' + nameOut + '.svg', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
	ff.savefig('./Manuscript/Figures/' + nameOut + '.pdf', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
	print('Done with ' + nameOut)
	return 0

if parallel is True:
	pool = multiprocessing.Pool()
	pool.map(runFunc, figList)
else:
	list(map(runFunc, figList))


# Overlay cartoon
template = st.fromfile('./Manuscript/Figures/Figure2.svg')
cartoon = st.fromfile('./recepmod/figures/Figure2_model_diagram.svg').getroot()

cartoon.moveto(10, -15)

template.append(cartoon)
template.save('./Manuscript/Figures/Figure2.svg')

# Output data table
StoneModelMouse().writeModelData('./Manuscript/Figures/ModelData.md')

