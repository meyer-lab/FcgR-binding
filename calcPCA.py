#!/usr/bin/env python3

from recepmod.PCAanalysis import recalcPCA
from recepmod.data.cellExprAndAct import geno

if __name__ == '__main__':
    for typ in geno:
        recalcPCA(typ)
