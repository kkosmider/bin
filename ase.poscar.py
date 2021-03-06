#!/usr/bin/python

import sys

import numpy as np 
from ase.io.vasp import read_vasp
from ase.io.vasp import write_vasp
from ase.io.xyz import write_xyz
from ase import Atoms

import asekk

from math import pi

from ase.constraints import FixAtoms


from optparse import OptionParser
from optparse import OptionGroup


parser = OptionParser()
parser.add_option("-f", "--format",           action="store", type="string", default="POSCAR",      help="format of the output file: POSCAR, (xyz in preparation)")
parser.add_option("-a", "--atoms",            action="store", type="int",    default=[-1,-1],       help="specify the atoms to whcih changes (translation rotation etc. will be made)", nargs=2)
parser.add_option("-p", "--periods",          action="store", type="int",    default=[1,1,1],       help="repetition of the unit cell", nargs=3)
parser.add_option("-T", "--Translation",      action="store", type="float",  default=[0.0,0.0,0.0], help="ss", nargs=3)

rotation =  OptionGroup(parser, "Rotation")
rotation.add_option("-r", "--rotation_angle",   action="store", type="float",  default=0.0,           help="rotation angle", nargs=1)
rotation.add_option(      "--rotate_around",    action="store", type="int",    default=0, help="rotate around nth atom", nargs=1)
parser.add_option_group(rotation)


cell =  OptionGroup(parser, "Cell")
#parser.add_option(      "--rotation_vector",  action="store", type="float",  default=[0.0,0.0,0.0], help="rotation point", nargs=1)
cell.add_option("-u", "--cell_scale",   action="store", type="float",  default=[1.0,1.0,1.0], help="unit cell scalling factor", nargs=3)
cell.add_option(      "--cell1_extend", action="store", type="float",  default=[0.0,0.0,0.0], help="unit cell scalling factor", nargs=3)
cell.add_option(      "--cell2_extend", action="store", type="float",  default=[0.0,0.0,0.0], help="unit cell scalling factor", nargs=3)
cell.add_option(      "--cell3_extend", action="store", type="float",  default=[0.0,0.0,0.0], help="unit cell scalling factor", nargs=3)

cell.add_option( "-u",
                 "--cell_scale",
                 action  = "store",
                 type    = "float", 
                 default = [1.0,1.0,1.0],
                 help    = "unit cell scalling factor",
                 nargs   = 3 )
cell.add_option(      "--cell1_extend", action="store", type="float",  default=[0.0,0.0,0.0], help="unit cell scalling factor", nargs=3)
cell.add_option(      "--cell2_extend", action="store", type="float",  default=[0.0,0.0,0.0], help="unit cell scalling factor", nargs=3)
cell.add_option(      "--cell3_extend", action="store", type="float",  default=[0.0,0.0,0.0], help="unit cell scalling factor", nargs=3)

parser.add_option_group(cell)

parser.add_option("-c", "--comment",          action="store", type="string", default=" ")
(options, args) = parser.parse_args()

#print parser.parse_args()

num = len(sys.argv)


if(num < 2):
    parser.print_help()
else:
    poscar = read_vasp(sys.argv[num-1])

    a = options.atoms # do not use/modify options.atoms
    natoms = poscar.get_number_of_atoms()
    if( a[0] > natoms or a[1] > natoms ):
        print "ERROR: a[0] > natoms | a[0] > natoms"
        exit()

    # atoms selection for modyfiactions
    if(a[0] == -1): # deafult case: we change all atoms
        a = (1, natoms)


    # --------------- Translations -----------------
    t = options.Translation
    is_translation_nonzero          = (t != (0.0,0.0,0.0))
    is_there_any_atoms_to_translate = (a[1]-a[0] >= 0)
    if( is_translation_nonzero and is_there_any_atoms_to_translate ):
        for i in range(a[0]-1, a[1]):
            poscar.arrays['positions'][i] +=  t


    # --------------- Rotation -----------------
    alpha  = options.rotation_angle
#    v      = options.rotation_vector

    if(alpha != 0.0):
        origin    = [0.0,0.0,0.0]
        ra        = options.rotate_around
        positions = poscar.arrays['positions']
        if(ra > 0 and ra <= natoms):
            origin  = positions[ra-1]
        origin = positions[options.rotate_around-1]
        
        # rotate selected atoms
        asekk.rotate_atoms(poscar, alpha, fromto=a, axis='z', origin=origin)


    # --------------- unit cell scaling facto -----------------
    u = options.cell_scale
    if( u != [1.0, 1.0, 1.0] ):
        c = poscar.get_cell()
        a = np.array(u)
        poscar.set_cell(c*a)

    # --------------- unit cell1 extending -----------------
    u = options.cell1_extend
    if( u != [0.0, 0.0, 0.0] ):
        c = poscar.get_cell()
        c[0] += np.array(u)
        poscar.set_cell(c)
    # --------------- unit cell2 extending -----------------
    u = options.cell2_extend
    if( u != [0.0, 0.0, 0.0] ):
        c = poscar.get_cell()
        c[1] += np.array(u)
        poscar.set_cell(c)
    # --------------- unit cell3 extending -----------------
    u = options.cell3_extend
    if( u != [0.0, 0.0, 0.0] ):
        c = poscar.get_cell()
        c[2] += np.array(u)
        poscar.set_cell(c)

    # --------------- Periodic repetitions -----------------
    p = options.periods
    if( p != [1,1,1]):
        poscar = poscar*(p[0], p[1], p[2])
#        print p


    # --------------- Wirting out in proper format -----------------
    if(options.format == "POSCAR"):
        write_vasp(sys.stdout,poscar,label=options.comment, direct=False,sort=False,vasp5=True)
    elif(options.format == "xyz"):
        write_xyz(sys.stdout,poscar,options.comment)
