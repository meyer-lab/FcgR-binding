#!/usr/bin/env python3

from recepmod.PCAanalysis import recalcPCA

geno = ['HIV','HIF','HTV','HTF','RIV','RIF','RTV','RTF']

if __name__ == '__main__':
    for typ in geno:
        recalcPCA(typ)
