input_file_path='/home/vanka/siddharth/molecular_machines_project/molecular_machines/verification/test_systems/ring_track_at_origin_non_ideal_artificial_system.xyz'
#input_file_path='/home/vanka/vipin/project_2_silane_aluminum_adduct/scanning_of_R_group_orientations/rc_for_ts_re_insertion_with_dcpdms_adduct_0_degree_dihedral.xyz'

output_dir_path='../output'

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


###################################***DO NOT MODIFY BELOW THIS LINE***##########################################
code_dir_path='core_code'
cd $code_dir_path
python main.py $input_file_path $output_dir_path $d_theta $ref_atom1_no $ref_atom2_no $atom_no_list
