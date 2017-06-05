from cellExprAndAct import cell, species, genotype

for cline in cell:
    for spec in species:
        for gen in genotype:
            if spec == 'murine':
                print('expressions["'+cline+'-'+spec+'-'+gen+'"] = [[1.0, 1.0, 1.0, 1.0],0]')
            else:
                print('expressions["'+cline+'-'+spec+'-'+gen+'"] = [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],1]')

print('\n')

for cline in cell:
    for spec in species:
        for gen in genotype:
            if gen == 'murine':
                print('activities["'+cline+'-'+spec+'-'+gen+'"] = [1.0, -1.0, 1.0, 1.0]')
            else:
                print('activities["'+cline+'-'+spec+'-'+gen+'"] = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]')
