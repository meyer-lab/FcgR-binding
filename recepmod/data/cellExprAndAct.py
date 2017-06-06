from numpy import nan

cell = ['NK','MO','DC']
##genotype = ['murine','human-Phe','human-Val']
genotype = ['Phe','Val']

expressions = {}
activities = {}

# Organized first by cell line, then by genotype.
# The first list is for murine, the second for human.
expressions["NK-Phe"] = [[1.0, 1.0, 0.0, 0.0],[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
expressions["NK-Val"] = [[1.0, 1.0, 0.0, 0.0],[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
expressions["MO-Phe"] = [[1.0, 1.0, 0.0, 0.0],[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
expressions["MO-Val"] = [[1.0, 1.0, 0.0, 0.0],[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
expressions["DC-Phe"] = [[1.0, 1.0, 0.0, 0.0],[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
expressions["DC-Val"] = [[1.0, 1.0, 0.0, 0.0],[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]


activities["NK-Phe"] = [[1.0, -1.0, nan, nan],[1.0, 1.0, 1.0, nan, nan, nan, nan, nan]]
activities["NK-Val"] = [[1.0, -1.0, nan, nan],[1.0, 1.0, 1.0, nan, nan, nan, nan, nan]]
activities["MO-Phe"] = [[1.0, -1.0, nan, nan],[1.0, 1.0, 1.0, nan, nan, nan, nan, nan]]
activities["MO-Val"] = [[1.0, -1.0, nan, nan],[1.0, 1.0, 1.0, nan, nan, nan, nan, nan]]
activities["DC-Phe"] = [[1.0, -1.0, nan, nan],[1.0, 1.0, 1.0, nan, nan, nan, nan, nan]]
activities["DC-Val"] = [[1.0, -1.0, nan, nan],[1.0, 1.0, 1.0, nan, nan, nan, nan, nan]]
