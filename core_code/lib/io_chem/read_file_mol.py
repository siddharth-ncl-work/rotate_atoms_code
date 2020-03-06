import numpy as np
import pandas as pd
from tqdm import tqdm
import networkx as nx


def getAtomCount(file_path,atom_no_digits=3):
  with open(file_path,'r') as file:
    file.readline()
    file.readline() 
    file.readline()
    line=file.readline()
    atoms=int(line[:atom_no_digits])
  return atoms

def getAtomDict(file_path,atom_no_digits=3):
  atom_dict={}
  file=open(file_path,'r')
  cords_df=getCords(file_path,atom_no_digits=atom_no_digits)
  for index,row in cords_df.iterrows():
    atom_no=row['atom_no']
    atom_name=row['atom']
    atom_dict[atom_no]=atom_name
  file.close()
  return atom_dict

def processLineCords(line):
  line=line.strip().split()
  line=line[:4]
  line[0]=float(line[0])
  line[1]=float(line[1])
  line[2]=float(line[2])
  return line

def processLineBonds(line,atom_no_digits=3):
  atom0=int(line[:atom_no_digits])-1
  atom1=int(line[atom_no_digits:2*atom_no_digits])-1
  line=[atom0,atom1,1]
  return line

def getCords(file_path,atom_no_digits=3):
  data={'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
  file=open(file_path,'r')
  file.readline()
  file.readline()
  file.readline()
  line=file.readline()
  atoms=int(line[:atom_no_digits])
  for i in range(atoms):
    line=file.readline()
    line=processLineCords(line)
    data['atom'].append(line[3])
    data['atom_no'].append(i)
    data['x'].append(line[0])
    data['y'].append(line[1])
    data['z'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  file.close()
  return df

def getBonds(file_path,atom_no_digits=3):
  data={'atom0_no':[],'atom1_no':[],'bond':[]}
  file=open(file_path,'r')
  file.readline()
  file.readline()
  file.readline()
  line=file.readline()
  atoms=int(line[:atom_no_digits])
  bonds=int(line[atom_no_digits:2*atom_no_digits])
  for i in range(atoms):
    file.readline()
  for i in range(bonds):
    line=file.readline()
    line=processLineBonds(line)
    data['atom0_no'].append(line[0])
    data['atom1_no'].append(line[1])
    data['bond'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  file.close()
  return df
  
def getCordsAndBonds(file_path,atom_no_digits=3):
  df_cords=pd.DataFrame(columns=['atom','atom_no','x','y','z'])
  df_bonds=pd.DataFrame(columns=['atom0_no','atom1_no','bond'])

  data_cords={'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
  file=open(file_path,'r')
  file.readline()
  file.readline()
  file.readline()
  line=file.readline()
  atoms=int(line.strip().split()[0])
  bonds=int(line.strip().split()[1])
  for i in range(atoms):
    line=file.readline()
    line=processLineCords(line)
    data_cords['atom'].append(line[3])
    data_cords['atom_no'].append(i)
    data_cords['x'].append(line[0])
    data_cords['y'].append(line[1])
    data_cords['z'].append(line[2])
    tmp_df_cords=pd.DataFrame.from_dict(data_cords)
    
  data_bonds={'atom0_no':[],'atom1_no':[],'bond':[]}
  for i in range(bonds):
    line=file.readline()
    line=processLineBonds(line)
    data_bonds['atom0_no'].append(line[0])
    data_bonds['atom1_no'].append(line[1])
    data_bonds['bond'].append(line[2])
  tmp_df_bonds=pd.DataFrame.from_dict(data_bonds)
    
  df_cords=pd.concat([df_cords,tmp_df_cords],ignore_index=True)
  df_bonds=pd.concat([df_bonds,tmp_df_bonds],ignore_index=True)
  file.close()
  return (df_cords,df_bonds)
  
def getAdjacencyMatrix(file_path,atom_no_digits=3):
  atom_count=getAtomCount(file_path)
  bonds_df=getBonds(file_path,atom_no_digits=atom_no_digits)
  adjacency_matrix=np.zeros((atom_count,atom_count))
  for index,row in bonds_df.iterrows():
    atom0=row['atom0_no']
    atom1=row['atom1_no']
    adjacency_matrix[atom0][atom1]=row['bond']
    adjacency_matrix[atom1][atom0]=row['bond']
  return adjacency_matrix

def getFrameGraph(file_path,atom_no_digits=3):
  atom_dict=getAtomDict(file_path,atom_no_digits=atom_no_digits)
  adjacency_matrix=getAdjacencyMatrix(file_path,atom_no_digits=atom_no_digits)
  G=nx.from_numpy_matrix(adjacency_matrix)
  nx.set_node_attributes(G,name='element',values=atom_dict)
  return G
