#!/usr/bin/env python3
import subprocess

begin_line = """units real
atom_style full
pair_style lj/cut/coul/long 10.0
bond_style      harmonic
angle_style     harmonic
dihedral_style  harmonic
improper_style  cvff
kspace_style	pppm 0.0001
neighbor 1.0 nsq
neigh_modify once no every 1 delay 0 check yes page 100000000 one 10000000
thermo 10

read_data comp_mob/co."""

end_line = """.data

# mod
# [1000, 1070, 1140, 1210, 1280, 1350, 1420, 1490, 1560]]
#poly
# [1560, 1752, 1944, 2136, 2328, 2520, 2712, 2904, 3096, 3288, 3480]

group molecule1 id 2329:2520

compute cmall all com
compute cmmol molecule1 com


thermo_style custom time c_cmall[1] c_cmall[2] c_cmall[3] c_cmmol[1] c_cmmol[2] c_cmmol[3]
thermo_modify norm no

#dump d1 all custom 100 c_cmall[1] c_cmall[2] c_cmall[3] c_cmmol[1] c_cmmol[2] c_cmmol[3]

fix 1 all npt temp 300.0 300.0 1000.0 x 0.0 0.0 1000 y 0.0 0.0 1000 z 0.0 0.0 1000

#print c_cmall[1] c_cmall[2] c_cmall[3] c_cmmol[1] c_cmmol[2] c_cmmol[3] file info.dat

run 0

unfix 1"""

f = open('1.data', 'w')

for j in range(1, 201):

    middle_line = str(j * 50000)

    lmp_file = open('lmp.in', 'w')
    lmp_file.write(begin_line)
    lmp_file.write(middle_line)
    lmp_file.write(end_line)
    lmp_file.close

    #variant 1
    proc = subprocess.Popen("lammps-daily < lmp.in", shell=True, stdout=subprocess.PIPE)
    out = proc.stdout.readlines()   

    flag = 0

    for line in out:
        line = line.decode()
        if line.startswith('Time c_cmall[1] c_cmall[2]'):
            flag = 1
            continue
        if flag == 1:
            #print(line)
            f.write(line)
            flag = 0
    proc.kill()
