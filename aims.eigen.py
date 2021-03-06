#!/usr/bin/python

######################################
#
#   Script which calculate average
#   efective potential basing on the
#   v_eff.dat file 
#
######################################
import sys
import numpy as np

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--fermi_in_zero",  action="store_true", default=False, help="If eigenvalues should be with Ferme lavel in the orgin")
(options, args) = parser.parse_args()

num = len(sys.argv)
f  = open(sys.argv[num-1], "r")
lines = f.read().splitlines()

# read: n - number od KS eigenvalues, index of laste eigenvalues bloc
n, index = 0, 0
fermi = 0.0
for i, line in enumerate(lines):
    if "Number of Kohn-Sham states (occupied + empty)" in line:
        l = line.split()
        n = int(l[8])
    if "State    Occupation    Eigenvalue [Ha]    Eigenvalue [eV]" in line:
        index=i+1
    if "Chemical potential (Fermi level) in eV" in line:
        l    = line.split()
        fermi = float(l[8])
    

if(index==0 and index < 0):
    print "ERROR: Eigenvalues has not been found"
    sys.exit()
else:
    eigens = []
    for i in range(index,index+n):
        l=lines[i].split()
        if(options.fermi_in_zero):
            eigens.append(float(l[3])-fermi)
        else:
            eigens.append(float(l[3]))

print 0.0, ' '.join(map(str, eigens))
print 1.0, ' '.join(map(str, eigens))

