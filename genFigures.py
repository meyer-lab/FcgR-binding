import svgutils.transform as st
from recepmod.figures import Figure1, Figure2, FigureSS, Figure3, Figure4, Figure5
from recepmod.StoneModMouse import StoneModelMouse

def runFunc(figClass, nameOut):
	print('Starting on ' + nameOut)
	ff = figClass.makeFigure()
	ff.savefig('./Manuscript/Figures/' + nameOut + '.svg', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
	ff.savefig('./Manuscript/Figures/' + nameOut + '.pdf', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)

runFunc(Figure1, 'Figure1')

runFunc(Figure2, 'Figure2')
template = st.fromfile('./Manuscript/Figures/Figure2.svg')
cartoon = st.fromfile('./recepmod/figures/Figure2_model_diagram.svg').getroot()

cartoon.moveto(10, -15)

template.append(cartoon)
template.save('./Manuscript/Figures/Figure2.svg')

runFunc(FigureSS, 'FigureSS')

runFunc(Figure3, 'Figure3')

runFunc(Figure4, 'Figure4')

StoneModelMouse().writeModelData('./Manuscript/Figures/ModelData.md')

runFunc(Figure5, 'Figure5')
