import pandas as pd 
import numpy as np
from decimal import Decimal
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from . import read_file_mol
from . import read_file_mol_md
from . import read_file_xyz
from . import read_file_xyz_md
from . import read_file_opt
from . import write_file_xyz
from . import write_file_xyz_md
from . import write_file_opt


def fileType(file):
  if type(file)==str:
    return file.strip().split('.')[-1].lower()
  else:
    return file.name.strip().split('.')[-1].lower()

def readFile(file_path,file_type=None,info='cords',atom_no_digits=3):
  if file_type==None:
    file_type=fileType(file_path)
  if file_type=='xyz':
    if info=='cords':
      df=read_file_xyz.getCords(file_path)
      return df
    elif info=='atom_count':
      atoms=read_file_xyz.totalAtoms(file_path)
      return atoms
  elif file_type=='mol':
    if info=='atom_count':
      atom_count=read_file_mol.getAtomCount(file_path,atom_no_digits=atom_no_digits)
      return atom_count
    elif info=='cords':
      df=read_file_mol.getCords(file_path,atom_no_digits=atom_no_digits)
      return df
    elif info=='bonds':
      df=read_file_mol.getBonds(file_path,atom_no_digits=atom_no_digits)
      return df
    elif info=='cords_and_bonds':
      dfs=read_file_mol.getCordsAndBonds(file_path,atom_no_digits=atom_no_digits)
      return dfs
    elif info=='adjacency_matrix':
      adjacency_matrix=read_file_mol.getAdjacencyMatrix(file_path,atom_no_digits=atom_no_digits)
      return adjacency_matrix
    elif info=='graph':
      graph=read_file_mol.getFrameGraph(file_path,atom_no_digits=atom_no_digits)
      return graph
    else:
      print('check info')
  elif file_type=='opt':
    if info=='cords':
      df=read_file_opt.getCords(file_path)
      return df
    elif info=='atoms':
      pass

def readFileMd(file,start_frame_no=0,end_frame_no=None,info='cords',file_type=None,frame_no_pos=1,atom_no_digits=3):
  if file_type==None:
    file_type=fileType(file)
  if file_type=='xyz':
    if info=='atoms':
      atoms=read_file_xyz_md.totalAtoms(file)
      return atoms
    elif info=='cords':
      df=read_file_xyz_md.getCords(file,start_frame_no,end_frame_no=end_frame_no,frame_no_pos=frame_no_pos)
      return df
    else:
      pass
  elif file_type=='mol':
    if info=='atom_count':
      atom_count=read_file_mol_md.getAtomCount(file)
      return atom_count
    elif info=='cords':
      df=read_file_mol_md.getCords(file,start_frame_no,end_frame_no=end_frame_no,frame_no_pos=frame_no_pos)
      return df
    elif info=='bonds':
      df=read_file_mol_md.getBonds(file,start_frame_no,end_frame_no=end_frame_no,atom_no_digits=atom_no_digits,frame_no_pos=frame_no_pos)
      return df
    elif info=='cords_and_bonds':
      dfs=read_file_mol_md.getCordsAndBonds(file,start_frame_no,end_frame_no=end_frame_no,atom_no_digits=atom_no_digits,frame_no_pos=frame_no_pos)
      return dfs
    elif info=='adjacency_matrix':
      adjacency_matrix_dict=read_file_mol_md.getAdjacencyMatrix(file,start_frame_no,end_frame_no=end_frame_no,atom_no_digits=atom_no_digits,frame_no_pos=frame_no_pos)
      return adjacency_matrix_dict
    elif info=='graph':
      graph_dict=read_file_mol_md.getFrameGraph(file,start_frame_no,end_frame_no=end_frame_no,atom_no_digits=atom_no_digits,frame_no_pos=frame_no_pos)
      return graph_dict
    else:
      print('check info')
  elif file_type=='opt':
    pass
  else:
    print('file type is not yet implemented')

def writeFile(file_path,df,file_type=None,info='normal',atoms_list=None):
  if file_type==None:
    file_type=fileType(file_path)
  if file_type=='xyz':
    if info=='normal':
      write_file_xyz.writeCords(file_path,df)
    elif info=='fix_atoms':
      pass
  elif file_type=='mol':
    pass
  elif file_type=='opt':
    if info=='normal':
      write_file_opt.writeCords(file_path,df)
    elif info=='fix_atoms':
      write_file_opt.fixAtoms(file_path,df,atoms_list)

def writeFileMd(file,df,frame_no,file_type=None,info='normal',atoms_list=None,frame_no_pos=1):
  if file_type==None:
    file_type=fileType(file)
  if file_type=='xyz':
    if info=='normal':
      write_file_xyz_md.writeCords(file,df,frame_no,frame_no_pos=frame_no_pos)
    elif info=='fix_atoms':
      pass
  elif file_type=='mol':
    pass
  elif file_type=='opt':
    pass


if __name__=='__main__':
  #file=open('/home/vanka/siddharth/mol_data/Acetamide3d.mol','r')
  #file_path='/home/vanka/siddharth/shailaja_project/Na_cluster_for_center_of_mass'
  #df=readFile(file_path,file_type='xyz')
  #file_path='/home/vanka/shailja/na_h20_with_in_4angstrom_from_md_now_aimd/scr/coors.xyz'
  mol_sd_file_path='test_systems/frames_0_1000.mol'
  
  with open(mol_sd_file_path,'r') as file:
    df=readFileMd(file,info='graph',frame_no_pos=2)
    pos=nx.spring_layout(df[0])
    nx.draw_networkx(df[0],pos,labels=nx.get_node_attributes(df[0],'element'))
    plt.show()
  
  '''
  file_path='test_systems/sugar.mol'
  df=readFile(file_path,info='graph')
  print(df)
  pos=nx.spring_layout(df)
  nx.draw_networkx(df,pos,labels=nx.get_node_attributes(df,'element'))
  plt.show()
  '''
