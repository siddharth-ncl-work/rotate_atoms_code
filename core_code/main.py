import sys
import os
import math
from tqdm import tqdm

from lib.io_chem import io
from source import rotation


def get_sys_agrs():
  input_file_path=sys.argv[1]
  output_dir_path=sys.argv[2]
  d_theta=int(sys.argv[3])
  ref_atom1_no=int(sys.argv[4])-1
  ref_atom2_no=int(sys.argv[5])-1
  atom_no_list=list(map(int,sys.argv[6:]))
  atom_no_list=list(map(lambda x:x-1,atom_no_list))
  args_dict={'input_file_path':input_file_path,'output_dir_path':output_dir_path,'d_theta':d_theta,'ref_atom1_no':ref_atom1_no,'ref_atom2_no':ref_atom2_no,'atom_no_list':atom_no_list}
  return args_dict

def getAxis(agrs_dict,cords_df):
  axis=[0,0,0]
  ref_atom1_no=args_dict['ref_atom1_no']
  ref_atom2_no=args_dict['ref_atom2_no']
  ref_atom1_cords=cords_df[cords_df['atom_no']==ref_atom1_no][['x','y','z']].values[0]
  ref_atom2_cords=cords_df[cords_df['atom_no']==ref_atom2_no][['x','y','z']].values[0]
  axis[0]=ref_atom2_cords[0]-ref_atom1_cords[0]
  axis[1]=ref_atom2_cords[1]-ref_atom1_cords[1]
  axis[2]=ref_atom2_cords[2]-ref_atom1_cords[2]
  return axis

args_dict=get_sys_agrs()
output_file_name=args_dict['input_file_path'].split('/')[-1].split('.')[0]
output_file_md=open(os.path.join(args_dict['output_dir_path'],output_file_name+f'_md.xyz'),'w')
initial_cords_df=io.readFile(args_dict['input_file_path'])
ref_atom1_no=args_dict['ref_atom1_no']
ref_atom1_cords=initial_cords_df[initial_cords_df['atom_no']==ref_atom1_no][['x','y','z']].values[0]
shifted_initial_cords_df=rotation.shiftOrigin(initial_cords_df,ref_atom1_cords)
axis=getAxis(args_dict,initial_cords_df)
for key,value in args_dict.items():
  print(f'{key} = {value}')
print(initial_cords_df.head())
print(f'rotation axis = {axis}')
for curr_frame_no,theta in enumerate(tqdm(range(0,360,args_dict['d_theta']))):
  final_cords_df=rotation.rotateAlongAxis(shifted_initial_cords_df,axis,math.radians(theta),args_dict['atom_no_list'])
  io.writeFile(os.path.join(args_dict['output_dir_path'],output_file_name+f'_{theta}.xyz'),final_cords_df)
  io.writeFileMd(output_file_md,final_cords_df,curr_frame_no,frame_no_pos=2)
