input_file_path=/home/vanka/vipin/project_2_silane_aluminum_adduct/scanning_of_R_group_orientations/rc_for_ts_re_insertion_with_dcpdms_adduct_0_degree_dihedral.xyz

output_dir_path=../output

d_theta=20

ref_atom1_no=6
ref_atom2_no=4

atom_no_list="
4
140
3
145
137
5
139
141
1
143
142
2
138
144
"


###################################***DO NOT MODIFY BELOW THIS LINE***##########################################
code_dir_path='core_code'
cd $code_dir_path
python main.py $input_file_path $output_dir_path $d_theta $ref_atom1_no $ref_atom2_no $atom_no_list
