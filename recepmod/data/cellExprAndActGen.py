from cellExprAndAct import cell, species

for cline in cell:
    for spec in species:
        print('expressions["'+cline+'-'+spec+'"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]')

print('\n')

for cline in cell:
    for spec in species:
        print('activities["'+cline+'-'+spec+'"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]')
