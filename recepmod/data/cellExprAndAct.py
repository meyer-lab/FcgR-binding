from numpy import nan

cell = ['NK','MO','DC']
species = ['murine','human-Phe','human-Val']

expressions = {}
activities = {}

# Organized first by cell line, then by genotype.
# The first list is for murine, the second for human.
expressions["NK"] = [[nan, 3.0, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, 3.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["MO"] = [[nan, 3.0, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, 3.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["DC"] = [[nan, 3.0, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, 3.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]


activities["NK"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["MO"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["DC"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
