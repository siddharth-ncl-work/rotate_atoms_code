file_path='/home/vanka/siddharth/molecular_machines_project/molecular_machines/verification/test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz'
d_theta=10
ref_atom1_no=21
ref_atom2_no=38
atom_no_list="
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
"

###############################################################
code_dir_path='core_code'
cd $code_dir_path
python main.py $file_path $d_theta $ref_atom1_no $ref_atom2_no $atom_no_list
