# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 10:04:09 2017

@author: mitadm
"""

#Editing StoneMod for CHO
import StoneModel
import numpy as np
from scipy.optimize import brentq
from scipy.misc import comb
from os.path import join

np.seterr(over = 'raise')


class StoneModelMouse:
    # Takes in a list of shape (9) for x: Rexp for FcgRs and TRIM21 logR, the kind of Ig, avidity Kx, valency uv, Immune Complex Concentration L0 
    def __init__(self):
        path = './Other Binding Data'
        self.Igs = ['IgG1', 'IgG2a', 'IgG2b', 'IgG3']
        self.FcgRs = ['FcgRI', 'FcgRIIB', 'FcgRIII', 'FcgRIV', 'FcgRn', 'TRIM21']
        # Read in csv file of murine binding affinities 
        self.kaMouse = np.genfromtxt(join(path,'murine-affinities.csv'), delimiter=',', skip_header=1, usecols=list(range(1,5)))
        # Indices for elements in x 
        self.IgIDX = 6
        self.kxIDX = 7
        self.uvIDX = 8
        self.L0IDX = 9

    def StoneModMouse(self, x, fullOutput = False):
        ## Returns the number of mutlivalent ligand bound to a cell with 10^logR
        ## receptors, granted each epitope of the ligand binds to the receptor
        ## kind in question with affinity Ka and cross-links with
        ## other receptors with crosslinking constant Kx = 10^logKx. All
        ## equations derived from Stone et al. (2001).
        
        # Assign Ig type to a number corresponding to the row of Ka            
        for i in range(4):
            if self.Igs[i] == x[self.IgIDX]:
                x[self.IgIDX] = i
        if type(x[self.IgIDX]) != int:
            return (np.nan, np.nan, np.nan)
        
        # Assign inputs for StoneMod
        x = np.array(x)
        l = int(x[self.IgIDX])
        v = x[self.uvIDX]
        Kx = np.power(10, x[self.kxIDX])
        L0 = x[self.L0IDX]
        
        # Initiate numpy arrays for StoneMod outputs 
        outputLbnd = np.full((6), np.nan)
        outputReq = np.full((6), np.nan)
        outputRbnd = np.full((6), np.nan)
                
        if fullOutput:
            outputRmulti = np.full((6), np.nan)
            outputnXlink = np.full((6), np.nan)
            
        # Iterate over each FcgR
        for k in range(6):
            logR = x[k]
            ## Set the affinity for the binding of the FcgR and IgG in question
            Ka = self.kaMouse[k][l]
            if Ka == '+' or Ka == 0:
                continue
            Ka = float(Ka)
            ## Calculate the MFI which should result from this condition according to the model
            stoneModOut = StoneModel.StoneMod(logR,Ka,v,Kx,L0, fullOutput = True)
            outputLbnd[k] = stoneModOut[0]
            outputRbnd[k] = stoneModOut[1] 
            outputReq[k] = stoneModOut[4]

            # Fill in Rmulti and nXlink for full output 
            if fullOutput:
                outputRmulti[k] = stoneModOut[2]
                outputnXlink[k] = stoneModOut[3]

        if fullOutput:
            return (outputLbnd, outputRbnd, outputRmulti, outputnXlink, outputReq)
