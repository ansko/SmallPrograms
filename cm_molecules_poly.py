#!/usr/bin/env python3

# good and works
# программа исключительно для работы с полимером
# где 30720 атомов

import math
import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint

folder = 'pa_mob_data2/'
masses = [ 
    0, # there is no 0 type
    1.00797,
    12.0112,
    1.00797,
    12.0112,
    15.9994,
    14.0067,
    14.0067,
    12.0112
]

# прочитать датафайл и вернуть атомы и границы в списке
def read_datafile(filename):
    f = open(filename, 'r')
    flag = 0
    atoms = []
    bounds = []

    atom = 0
    for line in f:
        if line.endswith('xlo xhi\n'):
            line_s = line.split()
            bounds.append(float(line_s[0]))
            bounds.append(float(line_s[1]))
        if line.endswith('ylo yhi\n'):
            line_s = line.split()
            bounds.append(float(line_s[0]))
            bounds.append(float(line_s[1]))
        if line.endswith('zlo zhi\n'):
            line_s = line.split()
            bounds.append(float(line_s[0]))
            bounds.append(float(line_s[1]))
        if line.startswith('Atoms # full'):
            flag = 1
            continue
        if line.startswith('Velocities'):
            break

        if flag == 1:
            line = line.split()
            atoms.append([])
            for word in line:
                try:
                    word = int(word)
                except:
                    word = float(word)
                atoms[atom].append(word)
            atom += 1
    atoms.pop(0)
    atoms.pop(len(atoms) - 1)
    atoms.sort()

    return (atoms, bounds)

# рассчитать координаты центра масс группы атомов
def calculate_com(atoms):
    mass = 0
    com = [0, 0, 0] # center-of-mass coordinates
    for atom in atoms:
        atom_type = atom[2]
        atom_mass = masses[atom_type]
        mass += atom_mass
        atom_x = atom[4]
        atom_y = atom[5]
        atom_z = atom[6]
        com[0] += atom_mass * atom_x
        com[1] += atom_mass * atom_y
        com[2] += atom_mass * atom_z
    com[0] /= mass
    com[1] /= mass
    com[2] /= mass

    return com

# рассчитать смещение с учётом возможного перехода границ задаются старые
# и новые координаты чего-то одного (атома или цм); границы ячейки
def calculate_disp(old, new, bounds=None):
    displacement=[0, 0, 0]
    bounds_def = [
        3.6574177352488846e-01, 9.3767139801735425e+01,
       -1.7173796716130170e+00, 7.8533787176849529e+01,
        4.2580775568494040e+00, 4.6615800720898385e+01
    ]
    if bounds is None:
        bounds = bounds_def
    # x
    delta = new[0] - old[0]
    delta2 = bounds[1] - bounds[0] - abs(delta)
    if abs(delta) < abs(delta2):
        displacement[0] += delta
    else:
        displacement[0] = -math.copysign(delta2, delta)
    # y
    delta = new[1] - old[1]
    delta2 = bounds[3] - bounds[2] - abs(delta)
    if abs(delta) < abs(delta2):
        displacement[1] += delta
    else:
        displacement[1] = -math.copysign(delta2, delta)
    # z
    delta = new[2] - old[2]
    delta2 = bounds[5] - bounds[4] - abs(delta)
    if abs(delta) < abs(delta2):
        displacement[2] += delta
    else:
        displacement[2] = -math.copysign(delta2, delta)

    return (displacement[0], displacement[1], displacement[2])

# формируется имя файла для чтения
def make_file_name(j):
    fname = folder + 'co.' + str(j * 50000) + '.data'
    return fname

# формируется список, состоящий из списков, в которых
# лежат номера атомов, относящихся к каждой молекуле
def make_molecules():
    molecules = []
    for mol_number in range(160):
        molecule = [mol_number * 192 + j + 1 for j in range(192)]
        molecules.append(molecule)
    return molecules
#-----------------------------------------------------------------------------

fname = make_file_name(1)
(atoms_start, bounds_start) = read_datafile(fname)

molecules = make_molecules()
molecules_com_disp = [[0, 0, 0, 0] for i in range(160)]
ave_disp = [0 for i in range(199)]
#exit()

for file_number in range(1, 198):
    fname_old = make_file_name(file_number)
    fname_new = make_file_name(file_number + 1)
    (atoms_old, bounds_old) = read_datafile(fname_old)
    (atoms_new, bounds_new) = read_datafile(fname_new)
    for mol_num in range(160):
        mol_atoms = molecules[mol_num]
        atoms_in_mol_new = []
        atoms_in_mol_old = []
        atoms_in_mol = []
        for i in range(len(atoms_old)):
            atom = atoms_old[i]
            atom_num = atom[0]
            if atom_num in mol_atoms:
                atoms_in_mol_old.append(atom)
            atom = atoms_new[i]
            atom_num = atom[0]
            if atom_num in mol_atoms:
                atoms_in_mol_new.append(atom)
        com_old = calculate_com(atoms_in_mol_old)
        com_new = calculate_com(atoms_in_mol_new)
        delta_com = calculate_disp(com_old, com_new, bounds_new)
        molecules_com_disp[mol_num][0] += delta_com[0]
        molecules_com_disp[mol_num][1] += delta_com[1]
        molecules_com_disp[mol_num][2] += delta_com[2]
        molecules_com_disp[mol_num][3] = molecules_com_disp[mol_num][0]**2
        molecules_com_disp[mol_num][3] += molecules_com_disp[mol_num][1]**2
        molecules_com_disp[mol_num][3] += molecules_com_disp[mol_num][2]**2
        #molecules_com_disp[mol_num][3] = math.sqrt(molecules_com_disp[mol_num][3])
    for k in range(160):
        ave_disp[file_number - 1] += molecules_com_disp[k][3]
    ave_disp[file_number - 1] /= 160
    print(ave_disp[file_number - 1])
