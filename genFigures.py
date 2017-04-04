import recepmod

def runFunc(figClass, nameOut):
    ff = figClass.makeFigure()
    ff.savefig('./Manuscript/Figures/' + nameOut + '.svg', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
    ff.savefig('./Manuscript/Figures/' + nameOut + '.pdf', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
runFunc(recepmod.figures.Figure1, 'Figure1')

runFunc(recepmod.figures.Figure2, 'Figure2')

runFunc(recepmod.figures.Figure3, 'Figure3')

runFunc(recepmod.figures.Figure4, 'Figure4')
