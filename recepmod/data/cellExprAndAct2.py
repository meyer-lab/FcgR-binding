from numpy import nan

cell = ['NK','MO','DC']
geno = ['human-Phe','human-Val']

expressions = {'human-Phe':{}, 'human-Val':{}}
activities = {'human-Phe':{}, 'human-Val':{}}

# Organized first by genotype, then by cell line.
# The first list is for murine, the second for human.
expressions["human-Phe"]["NK"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
expressions["human-Phe"]["MO"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
expressions["human-Phe"]["DC"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
activities["human-Phe"]["NK"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]
activities["human-Phe"]["MO"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]
activities["human-Phe"]["DC"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]


expressions["human-Val"]["NK"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
expressions["human-Val"]["MO"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
expressions["human-Val"]["DC"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
activities["human-Val"]["NK"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]
activities["human-Val"]["MO"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]
activities["human-Val"]["DC"] = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]
