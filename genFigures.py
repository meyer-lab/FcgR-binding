from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from recepmod.figures import Figure1
from recepmod.figures import Figure2
from recepmod.figures import Figure3
from recepmod.figures import Figure4
from recepmod.figures import Figure5

def runFunc(figClass, nameOut):
    ff = figClass.makeFigure()
    ff.savefig('./Manuscript/Figures/' + nameOut + '.svg', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
    ff.savefig('./Manuscript/Figures/' + nameOut + '.pdf', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
runFunc(Figure1, 'Figure1')

runFunc(Figure2, 'Figure2')

runFunc(Figure3, 'Figure3')
