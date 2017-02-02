from matplotlib.backends.backend_pdf import PdfPages
from recepmod.figures import Figure1
from recepmod.figures import Figure2
from recepmod.figures import Figure3
from recepmod.figures import Figure4
from recepmod.figures import Figure5

f = Figure1.makeFigure()

with PdfPages('Figure1.pdf') as pdf:
    pdf.savefig(f)
