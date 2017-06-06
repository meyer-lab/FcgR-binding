from cellExprAndAct import cell, species

for cline in cell:
    print('expressions["'+cline+'"] = [[nan, 3.0, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, 3.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]')

print('\n')

for cline in cell:
    print('activities["'+cline+'"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]')
