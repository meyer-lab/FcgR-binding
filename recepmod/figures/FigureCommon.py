import seaborn as sns

figList = ['Figure1', 'Figure2', 'Figure3', 'Figure4', 'Figure5', 'FigureSS']

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

FcgRidx = ['FcgRI', 'FcgRIIA-Arg', 'FcgRIIA-His', 'FcgRIIB', 'FcgRIIIA-Phe', 'FcgRIIIA-Val']
FcgRidx = dict(zip(FcgRidx, sns.color_palette()))

FcgRTex = [r'Fc$\gamma$RI', r'Fc$\gamma$RIIA-Arg', r'Fc$\gamma$RIIA-His', r'Fc$\gamma$RIIB', r'Fc$\gamma$RIIIA-Phe', r'Fc$\gamma$RIIIA-Val']

FcgRidxL = [r'Fc$\gamma$RI',r'Fc$\gamma$RIIA-131R',r'Fc$\gamma$RIIA-131H',r'Fc$\gamma$RIIB',r'Fc$\gamma$RIIIA-158F',r'Fc$\gamma$RIIIA-158V']
FcgRidxL = dict(zip(FcgRidxL, sns.color_palette()))

def makeFcIgLegend():
    import matplotlib.lines as mlines
    import matplotlib.patches as mpatches

    patches = list()

    for f in FcgRidxL:
        patches.append(mpatches.Patch(color=FcgRidxL[f], label=f))

    for j in Igs:
        patches.append(mlines.Line2D([], [], color='black', marker=Igs[j], markersize=7, label=j, linestyle='None'))

    return patches

def subplotLabel(ax, letter):
    ax.text(-0.2, 1.2, letter, transform=ax.transAxes, fontsize=16, fontweight='bold', va='top')
