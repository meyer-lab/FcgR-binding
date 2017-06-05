cell = ['NK','MO','DC']
genotype = ['murine','human-Phe','human-Val']

expressions = {}
activities = {}

# Organized first by cell line, then by genotype
expressions["NK-murine"] = [1.0, 1.0, 1.0, 1.0]
expressions["NK-human-Phe"] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
expressions["NK-human-Val"] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
expressions["MO-murine"] = [1.0, 1.0, 1.0, 1.0]
expressions["MO-human-Phe"] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
expressions["MO-human-Val"] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
expressions["DC-murine"] = [1.0, 1.0, 1.0, 1.0]
expressions["DC-human-Phe"] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
expressions["DC-human-Val"] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

activities["NK-murine"] = [1.0, -1.0, 1.0, 1.0]
activities["NK-human-Phe"] = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
activities["NK-human-Val"] = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
activities["MO-murine"] = [1.0, -1.0, 1.0, 1.0]
activities["MO-human-Phe"] = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
activities["MO-human-Val"] = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
activities["DC-murine"] = [1.0, -1.0, 1.0, 1.0]
activities["DC-human-Phe"] = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
activities["DC-human-Val"] = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
