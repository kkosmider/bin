#!/usr/bin/python
import sys

from ase.io.aims import write_aims
from ase.io.cube import write_cube
from ase.io.vasp import write_vasp
from ase.io.xsf  import write_xsf
from ase.io.xyz  import write_xyz
from ase.lattice.cubic import FaceCenteredCubic

from optparse import OptionParser


parser = OptionParser()
parser.add_option("-a", "--lattice",    action="store",       type="float", default=1.0)
parser.add_option("-p", "--periods",          action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
parser.add_option("-e", "--element",    action="store", type="string", default='H')
(options, args) = parser.parse_args()


a=options.lattice
p=options.periods
e=options.element

#print a

atoms = FaceCenteredCubic(latticeconstant=a, directions=[[1,0,0], [0,1,0], [0,0,1]], size=p, symbol=e, pbc=(1,1,1))

write_aims("geometry.in", atoms)
