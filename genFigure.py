#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    nameOut = 'Figure' + sys.argv[1]
    exec('from recepmod.figures import ' + nameOut)
    ff = eval(nameOut + '.makeFigure()')
    ff.savefig('./Manuscript/Figures/' + nameOut + '.svg', dpi=ff.dpi, bbox_inches='tight', pad_inches=0)
    print(nameOut + ' is done.')
