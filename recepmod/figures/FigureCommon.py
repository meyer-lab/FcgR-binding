import seaborn as sns

figList = ['Figure1', 'Figure2', 'Figure3', 'Figure4', 'Figure5', 'FigureSS']

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

FcgRidx = dict(zip(['FcgRI',
                    'FcgRIIA-Arg',
                    'FcgRIIA-His',
                    'FcgRIIB',
                    'FcgRIIIA-Phe',
                    'FcgRIIIA-Val'], sns.color_palette()))

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

FcgRidxL = dict(zip([r'Fc$\gamma$RI',
                     r'Fc$\gamma$RIIA-131R',
                     r'Fc$\gamma$RIIA-131H',
                     r'Fc$\gamma$RIIB',
                     r'Fc$\gamma$RIIIA-158F',
                     r'Fc$\gamma$RIIIA-158V'], sns.color_palette()))

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

def Legend(colors, shapes):
    """ Make legend. """
    import matplotlib
    
    patches = list()

    for key, val in colors.items():
        patches.append(matplotlib.patches.Patch(color=val, label=key))

    for key, val in shapes.items():
        patches.append(matplotlib.lines.Line2D([], [], color='black', marker=val, markersize=7, label=key, linestyle='None'))
    
    return patches