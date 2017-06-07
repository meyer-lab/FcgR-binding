from cellExprAndAct import cell, geno

for cline in cell:
    print('expressions["'+cline+'"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]')

print('\n')

for cline in cell:
    print('activities["'+cline+'"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]')
