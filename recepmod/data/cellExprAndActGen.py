from cellExprAndAct2 import cell, geno

for typ in geno:
    for cline in cell:
        print('expressions["'+typ+'"]["'+cline+'"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]')

    for cline in cell:
        print('activities["'+typ+'"]["'+cline+'"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]')

    print('\n')

