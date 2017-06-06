from numpy import nan

cell = ['NK','MO','DC']
species = ['murine','human-Phe','human-Val']

expressions = {}
activities = {}

# Organized first by cell line, then by genotype.
# The first list is for murine, the second for human.
expressions["NK"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
expressions["MO"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
expressions["DC"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]


activities["NK"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]
activities["MO"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]
activities["DC"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]
