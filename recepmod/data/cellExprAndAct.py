from numpy import nan

cell = ['NK','MO','DC']
species = ['murine','human-Phe','human-Val']

expressions = {}
activities = {}

# Organized first by cell line, then by genotype.
# The first list is for murine, the second for human.
expressions["NK-murine"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["NK-human-Phe"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["NK-human-Val"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["MO-murine"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["MO-human-Phe"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["MO-human-Val"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["DC-murine"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["DC-human-Phe"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]
expressions["DC-human-Val"] = [[nan, nan, 4.0, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan],[nan, nan, nan, nan, nan, 4.0, nan, nan]]


activities["NK-murine"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["NK-human-Phe"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["NK-human-Val"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["MO-murine"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["MO-human-Phe"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["MO-human-Val"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["DC-murine"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["DC-human-Phe"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
activities["DC-human-Val"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0],[1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]]
