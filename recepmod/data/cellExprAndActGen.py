from cellExprAndAct import cell, genotype

for cline in cell:
    for gen in genotype:
        print('expressions["'+cline+'-'+gen+'"] = [[1.0, 1.0, 0.0, 0.0],[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]')

print('\n')

for cline in cell:
    for gen in genotype:
        print('activities["'+cline+'-'+gen+'"] = [[1.0, -1.0, nan, nan],[1.0, 1.0, 1.0, nan, nan, nan, nan, nan]]')
