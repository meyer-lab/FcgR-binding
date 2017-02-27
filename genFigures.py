from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from recepmod.figures import Figure1
from recepmod.figures import Figure2
from recepmod.figures import Figure3
from recepmod.figures import Figure4
from recepmod.figures import Figure5

def runFunc(figClass, nameOut):
    with PdfPages('./Manuscript/Figures/' + nameOut + '.pdf') as pdf:
        ff = figClass.makeFigure()
        ff.savefig('./Manuscript/Figures/' + nameOut + '.svg')
        pdf.savefig(ff)

runFunc(Figure1, 'Figure1')

runFunc(Figure2, 'Figure2')

runFunc(Figure3, 'Figure3')
