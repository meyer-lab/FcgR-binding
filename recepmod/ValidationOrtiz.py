import pandas as pd
import numpy as np
from .StoneTwoRecep import StoneTwo

class Ortiz:
    def __init__(self):
        import os

        ## Find path for csv files, on any machine wherein the repository recepnum1 exists.
        path = os.path.dirname(os.path.abspath(__file__))
        self.Igs = ['IgG1', 'IgG2', 'IgG3', 'IgG4']
        self.FcgRs = ['FcgRI', 'FcgRIIA-Arg', 'FcgRIIA-His', 'FcgRIIB', 'FcgRIIIA-Phe', 'FcgRIIIA-Val']

        ## Define the matrix of Ka values from Bruhns
        self.kaBruhns = np.loadtxt(os.path.join(path,'./data/FcgR-Ka-Bruhns.csv'), delimiter=',')

        ## The valency and names of the different species
        self.valency = np.array([1, 2, 3, 3, 5, 5], dtype = np.int)
        self.structs = ['Fc1', 'Fc2', 'Fc3Y', 'Fc3L', 'Fc5X', 'Fc5Y']

        ## Read in the Fc responses
        self.FcResponse = pd.read_csv(os.path.join(path,'./data/ortiz/Fig2DE-response.csv'), comment='#')

    def predictResponse(self):
        ''' Predict the response measured. '''

        KaOne = self.kaBruhns[0][0] # The affinity of the relevant interaction
        KaTwo = self.kaBruhns[0][0] # The affinity of the relevant interaction
        L0 = 1E-4 # This is known

        logR = [2, 3]

        Kx = 1E-9

        #a = StoneTwo(logR, Ka, Kx)

        #outt = list()

        #for ii in range(len(self.structs)):
        #    outt = outt.append(a.getAllProps(self.valency[ii], L0))

        #print(outt)



