from temp2 import cell, genotype

for cline in cell:
    for gen in genotype:
        if gen == 'murine':
            print('expressions["'+cline+'-'+gen+'"] = [1.0, 1.0, 1.0, 1.0]')
        else:
            print('expressions["'+cline+'-'+gen+'"] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]')

print('\n')

for cline in cell:
    for gen in genotype:
        if gen == 'murine':
            print('activities["'+cline+'-'+gen+'"] = [1.0, -1.0, 1.0, 1.0]')
        else:
            print('activities["'+cline+'-'+gen+'"] = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]')
