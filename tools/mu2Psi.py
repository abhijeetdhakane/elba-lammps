#!/usr/bin/env python

# Script:  mu2Psi.py
# Purpose: This script reads a file containing a dipole projection profile
#          and calculates the corresponding electrostatic potential (Psi).
# Syntax:  mu2Psi.py inputFile area
#          inputFile = LAMMPS output file generated by fix ave/spatial
#          area = surface area of slabs in Angstrom^2
# Example: ./mu2Psi.py muDensZ.profile 4630 > elPotDip.dat
# Author:  Mario Orsi (orsimario at gmail.com)

import sys,os,string

if len(sys.argv) != 3:
  print "Syntax: mu2Psi.py inputFile area"
  sys.exit()

inFileName = sys.argv[1]
A_in_m = 1e-10 # angstrom in meter
area = float(sys.argv[2]) * A_in_m**2
inFile = open(inFileName, "r")
lines = inFile.readlines()
inFile.close()
eps0 = 8.854e-12 # [C/(Vm)] permittivity of free space
e_in_C = 1.6021766e-19 # magnitude of electron charge in Coulomb

# find bin thickness (delta):
for line in lines:
    if line[0] != '#': # ignore comments
        words = string.split(line)
        if len(words) == 2:
            nBins = int(words[1])
        if len(words) == 4:
            if int(words[0]) == 1:
                coordLower = float(words[1])
            if int(words[0]) == nBins:
                coordUpper = float(words[1])
delta = abs( coordUpper - coordLower ) * A_in_m / ( nBins - 1 )
slabVolume = area * delta

# calculate and output electric field:
muProjInt = 0.0
for line in lines:
    if line[0] != '#': # ignore comments
        words = string.split(line)
        if len(words) == 4:
            coord = float(words[1])
            muProj = float(words[2])*float(words[3])*e_in_C*A_in_m/slabVolume
            muProjInt = muProjInt + delta * muProj
            elPot = muProjInt / eps0
            print coord, elPot # [A, V]
    

