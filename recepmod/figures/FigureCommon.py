import seaborn as sns
import numpy as np
from ..StoneModel import StoneModel


IgList = ['IgG1', 'IgG2', 'IgG3', 'IgG4']


def iggRename(name):
    return 'h' + name


Igs = {'IgG1': 'o', 'IgG2': 'd', 'IgG3': 's', 'IgG4': '^'}
keys = [key for key in Igs.keys()]
for key in keys:
    Igs[iggRename(key)] = Igs[key]

FcgRlist = ['FcgRI',
            'FcgRIIA-Arg',
            'FcgRIIA-His',
            'FcgRIIB',
            'FcgRIIIA-Phe',
            'FcgRIIIA-Val']

FcgRidx = dict(zip(FcgRlist, sns.color_palette()))


def texRename(name):
    name = r'$K_x^*$' if name == 'Kx1' else name
    name = 'TNP-4 c.f.' if name == 'sigConv1' else name
    name = 'TNP-26 c.f.' if name == 'sigConv2' else name
    name = r'$\sigma_1^*$' if name == 'sigma' else name
    name = r'$\sigma_2^*$' if name == 'sigma2' else name
    name = r'$f_4$' if name == 'gnu1' else name
    name = r'$f_{26}$' if name == 'gnu2' else name
    name = r'hFc$\gamma$RI' if name == 'Rexp1' else name
    name = r'hFc$\gamma$RIIA-131R' if name == 'Rexp2' else name
    name = r'hFc$\gamma$RIIA-131H' if name == 'Rexp3' else name
    name = r'hFc$\gamma$RIIB' if name == 'Rexp4' else name
    name = r'hFc$\gamma$RIIIA-158F' if name == 'Rexp5' else name
    name = r'hFc$\gamma$RIIIA-158V' if name == 'Rexp6' else name
    name = r'hFc$\gamma$RI' if name == 'FcgRI' else name
    name = r'hFc$\gamma$RIIA-131R' if name == 'FcgRIIA-Arg' else name
    name = r'hFc$\gamma$RIIA-131H' if name == 'FcgRIIA-His' else name
    name = r'hFc$\gamma$RIIB' if name == 'FcgRIIB' else name
    name = r'hFc$\gamma$RIIIA-158F' if name == 'FcgRIIIA-Phe' else name
    name = r'hFc$\gamma$RIIIA-158V' if name == 'FcgRIIIA-Val' else name
    name = r'hFc$\gamma$RI' if name == r'Fc$\gamma$RIA' else name
    name = r'hFc$\gamma$RIIA-131R' if name == r'Fc$\gamma$RIIA-131R' else name
    name = r'hFc$\gamma$RIIA-131H' if name == r'Fc$\gamma$RIIA-131H' else name
    name = r'hFc$\gamma$RIIB' if name == r'Fc$\gamma$RIIB' else name
    name = r'hFc$\gamma$RIIIA-158F' if name == r'Fc$\gamma$RIIIA-158F' else name
    name = r'hFc$\gamma$RIIIA-158V' if name == r'Fc$\gamma$RIIIA-158V' else name
    return name


def texRenameList(names):
    return [texRename(name) for name in names]


FcgRlistL = texRenameList(FcgRlist)

FcgRidxL = dict(zip(FcgRlistL, sns.color_palette()))


def subplotLabel(ax, letter, hstretch=1):
    ax.text(-0.2 / hstretch, 1.2, letter, transform=ax.transAxes,
            fontsize=16, fontweight='bold', va='top')


def getSetup(figsize, gridd, mults=[], multz={}, empts=[]):
    from matplotlib import gridspec, pyplot as plt

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Setup plotting space
    f = plt.figure(figsize=figsize)

    # Make grid
    gs1 = gridspec.GridSpec(*gridd)

    # Get list of axis objects
    if not mults:
        ax = [f.add_subplot(gs1[x]) for x in range(gridd[0] * gridd[1])]
    else:
        ax = [f.add_subplot(gs1[x]) if x not in mults else f.add_subplot(gs1[x:x + multz[x]]) for x in range(
            gridd[0] * gridd[1]) if not any([x - j in mults for j in range(1, max(multz.values()))]) and x not in empts]

    return (ax, f)


def Legend(fcgrs, colorsDict, iglist, shapes):
    """ Make legend. """
    import matplotlib

    patches = list()

    for key, val in zip(fcgrs, [colorsDict[fcgr] for fcgr in fcgrs]):
        patches.append(matplotlib.patches.Patch(color=val, label=key))
    for key, val in zip(iglist, [shapes[ig] for ig in iglist]):
        patches.append(matplotlib.lines.Line2D([], [], markeredgecolor='black', markeredgewidth=1.0,
                                               markerfacecolor='black', marker=val, markersize=7,
                                               label=key, linestyle='None'))

    return patches


def getRquant():
    return StoneModel(newData=True).Rquant


def PCApercentVar(explainedVar, axes=None):
    """
    Takes in the vector of explained variance and a list of 2 ints as axis handle.
    Outputs labels, a list of len(2) for axis labels
    """
    if axes is None:
        percentVar = ['%.0f' % j for j in explainedVar[0:2] * 100]
        labels = ['PC 1 (' + percentVar[0] + '%)', 'PC 2 (' + percentVar[1] + '%)']
    else:
        percentVar = ['%.0f' % j for j in [explainedVar[
            axes[0] - 1] * 100, explainedVar[axes[1] - 1] * 100]]
        labels = [('PC ' + str(axes[0]) + '(' + percentVar[0] + '%)'),
                  ('PC ' + str(axes[1]) + '(' + percentVar[1] + '%)')]
    return labels


def alternatingRects(xlims, ylims, numRects, ax, color=(0.8, 0.8, 0.8)):
    from matplotlib.patches import Rectangle

    scale = (xlims[1] - xlims[0]) / numRects
    rectEdges = np.arange(xlims[0], xlims[1] + scale, scale)

    prerects = []
    for child in ax.get_children():
        if str(child)[0] == 'R':
            prerects.append(child)

    rects = []
    for j in range(len(rectEdges) - 2):
        if j % 2 == 1:
            rects.append(Rectangle((rectEdges[j], ylims[0]),
                                   rectEdges[j + 1] - rectEdges[j],
                                   ylims[1], color=color))
    for patch in rects:
        ax.add_patch(patch)

    for child in ax.get_children():
        if str(child)[0:6] == 'Line2D':
            ax.add_line(child)

    for patch in prerects:
        if str(patch) != 'Rectangle(xy=(0, 0), width=1, height=1, angle=0)':
            ax.add_patch(patch)


def overlayCartoon(figFile, cartoonFile, x, y, scalee=1):
    """ Add cartoon to a figure file. """
    import svgutils.transform as st

    # Overlay Figure 4 cartoon
    template = st.fromfile(figFile)
    cartoon = st.fromfile(cartoonFile).getroot()

    cartoon.moveto(x, y, scale=scalee)

    template.append(cartoon)
    template.save(figFile)
