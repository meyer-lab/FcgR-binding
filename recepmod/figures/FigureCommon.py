import seaborn as sns

figList = ['Figure1', 'Figure2', 'Figure3', 'Figure4', 'Figure5', 'FigureSS']

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

FcgRidx = ['FcgRI', 'FcgRIIA-Arg', 'FcgRIIA-His', 'FcgRIIB', 'FcgRIIIA-Phe', 'FcgRIIIA-Val']
FcgRidx = dict(zip(FcgRidx, sns.color_palette()))

FcgRTex = [r'Fc$\gamma$RI', r'Fc$\gamma$RIIA-Arg', r'Fc$\gamma$RIIA-His', r'Fc$\gamma$RIIB', r'Fc$\gamma$RIIIA-Phe', r'Fc$\gamma$RIIIA-Val']

def texRename(name):
    name = r'K$_x$' if name=='Kx1' else name
    name = 'TNP-4 c.f.' if name=='sigConv1' else name
    name = 'TNP-26 c.f.' if name=='sigConv2' else name
    name = r'$\sigma_1$' if name=='sigma' else name
    name = r'$\sigma_2$' if name=='sigma2' else name
##    name = 'TNP-4 effective avidity' if name=='gnu1' else name
##    name = 'TNP-26 effective avidity' if name=='gnu2' else name
    name = r'$\nu_4$' if name=='gnu1' else name
    name = r'$\nu_{26}$' if name=='gnu2' else name
    return name

def texRenameList(names):
    return [texRename(name) for name in names]

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

def getSetup(figsize, gridd):
    from matplotlib import gridspec
    import matplotlib.pyplot as plt

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Setup plotting space
    f = plt.figure(figsize=figsize)

    # Make grid
    gs1 = gridspec.GridSpec(*gridd)

    # Get list of axis objects
    ax = [f.add_subplot(gs1[x]) for x in range(gridd[0] * gridd[1])]

    return (ax, f)