from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from recepmod.figures import Figure1
from recepmod.figures import Figure2
from recepmod.figures import Figure3
from recepmod.figures import Figure4
from recepmod.figures import Figure5

with PdfPages('./Manuscript/Figures/Figure1.pdf') as pdf:
    pdf.savefig(Figure1.makeFigure())

with PdfPages('./Manuscript/Figures/Figure2.pdf') as pdf:
    pdf.savefig(Figure2.makeFigure())

with PdfPages('./Manuscript/Figures/Figure3.pdf') as pdf:
    pdf.savefig(Figure3.makeFigure())
