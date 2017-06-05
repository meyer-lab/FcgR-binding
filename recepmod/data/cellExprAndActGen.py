from cellExprAndAct import cell, genotype

for cline in cell:
    for gen in genotype:
        print('expressions["'+cline+'-'+gen+'"] = [[1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]')

for cline in cell:
    for gen in genotype:
        print('activities["'+cline+'-'+gen+'"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]')
