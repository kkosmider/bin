#!/usr/bin/python

import sys

from ase.io.vasp import read_vasp
from ase.io.vasp import write_vasp
from ase.io.xyz import write_xyz

from optparse import OptionParser


parser = OptionParser()
parser.add_option("-g", "--get",     action="store", type="string", default="positions",      help="what kind of data shoud be extracted")
#parser.add_option("-f", "--format",           action="store", type="string", default="POSCAR",      help="format of the output file: POSCAR, (xyz in preparation)")
parser.add_option("-a", "--atoms",            action="store", type="int",    default=[-1,-1],       help="specify the atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
#parser.add_option("-p", "--periods",          action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
#parser.add_option("-T", "--Translation",      action="store", type="float",  default=[0.0,0.0,0.0], help="ss", nargs=3)
#parser.add_option("-u", "--cell_scale",       action="store", type="float",  default=[1.0,1.0,1.0],           help="unit cell scalling factor", nargs=3)
#parser.add_option("-c", "--comment",          action="store", type="string", default=" ")
(options, args) = parser.parse_args()

#print parser.parse_args()

num = len(sys.argv)
poscar = read_vasp(sys.argv[num-1])

a = options.atoms # do not use/modify options.atoms
natoms = poscar.get_number_of_atoms()

if( a[0] == -1 and a[1] -1 ):
    print "ERROR: You have not specified atoms"
    sys.exit()
if( a[0] > natoms or a[1] > natoms ):
    print "ERROR: a[0] > natoms | a[1] > natoms"
    sys.exit()
if( a[0] < 1 or a[1] < 1 ):
    print "ERROR: a[0] < 1 or a[1] < 1"
    sys.exit()

r1 = poscar.get_positions()[a[0]-1]
r2 = poscar.get_positions()[a[1]-1]
dr = r2-r1


if(options.get == "pos_diff"):
    print r1
    print r2
    print dr[0], dr[1], dr[2]

#    # --------------- Translations -----------------
#    t = options.Translation
#    is_translation_nonzero          = (t != (0.0,0.0,0.0))
#    is_there_any_atoms_to_translate = (a[1]-a[0] > 0)
#    if( is_translation_nonzero and is_there_any_atoms_to_translate ):
#        for i in range(a[0]-1, a[1]):
#            poscar.arrays['positions'][i] +=  t


#    # --------------- unit cell scaling facto -----------------
#    u = options.cell_scale
#    if( u != [1.0, 1.0, 1.0] ):
#        cell = poscar.get_cell()
#        poscar.set_cell(cell*u)

#    # --------------- Periodic repetitions -----------------
#    p = options.periods
#    if( p != [1,1,1]):
#        poscar = poscar*(p[0], p[1], p[2])
##        print p


#    # --------------- Wirting out in proper format -----------------
#    if(options.format == "POSCAR"):
#        write_vasp(sys.stdout,poscar,label=options.comment, direct=False,sort=False,vasp5=True)
#    elif(options.format == "xyz"):
#        write_xyz(sys.stdout,poscar,options.comment)
