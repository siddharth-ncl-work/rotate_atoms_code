import numpy as np
import pandas as pd
from tqdm import tqdm
import networkx as nx


def getAtomCount(file,atom_no_digits=3):
  last_pos=file.tell()
  line=file.readline()
  while 'frame' not in line:
    line=file.readline()
  line=file.readline()
  line=file.readline() 
  line=file.readline()
  atoms=int(line[:atom_no_digits])
  file.seek(last_pos)
  return atoms

def getAtomDict(file,frame_no=None,atom_no_digits=3,frame_no_pos=2):
  atom_dict={}
  if frame_no!=None and frame_no<0:
    print('negative frame numbers are not allowed')
    return atom_dict
  last_pos=file.tell()
  if frame_no==None:
    line=file.readline()
    while 'frame' not in line:
      line=file.readline()
    frame_no=int(line.strip().split()[frame_no_pos])
  cords_df=getCords(file,frame_no+1,atom_no_digits=atom_no_digits,frame_no_pos=frame_no_pos)
  for index,row in cords_df.iterrows():
    atom_no=row['atom_no']
    atom_name=row['atom']
    atom_dict[atom_no]=atom_name
  file.seek(last_pos)
  return atom_dict

def gotoFrame(file,frame_no,frame_no_pos=2):
  line=file.readline()
  while line!='':
    if 'frame' in line:
      curr_frame_no=int(line.strip().split()[frame_no_pos])
      if curr_frame_no==frame_no:
        return (line,True)
    line=file.readline()    
  return line,False

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

def getCords(file,start_frame_no,end_frame_no=None,atom_no_digits=3,frame_no_pos=2):
  data={'frame':[],'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
 
  if end_frame_no!=None and end_frame_no<start_frame_no:
    return pd.DataFrame.from_dict(data)
    
  if end_frame_no==None:
    end_frame_no=start_frame_no

  for frame_no in range(start_frame_no,end_frame_no+1):
    line,succ=gotoFrame(file,frame_no,frame_no_pos=frame_no_pos)
    if not succ:
      print('-->Could not find the frame {}'.format(start_frame_no))
      continue
    elif succ:
      curr_frame_no=int(line.strip().split()[frame_no_pos])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      line=file.readline()
      line=file.readline()
      line=file.readline()
      atoms=int(line[:atom_no_digits])
      for i in range(atoms):
        line=file.readline()
        line=processLineCords(line)
        data['frame'].append(curr_frame_no)
        data['atom'].append(line[3])
        data['atom_no'].append(i)
        data['x'].append(line[0])
        data['y'].append(line[1])
        data['z'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  return df

def getBonds(file,start_frame_no,end_frame_no=None,atom_no_digits=3,frame_no_pos=2):
  data={'frame':[],'atom0_no':[],'atom1_no':[],'bond':[]}
 
  if end_frame_no!=None and end_frame_no<start_frame_no:
    return pd.DataFrame.from_dict(data)
  
  if end_frame_no==None:
    end_frame_no=start_frame_no
    
  for frame_no in range(start_frame_no,end_frame_no+1):
    line,succ=gotoFrame(file,frame_no,frame_no_pos=frame_no_pos)
    if not succ:
      print('Could not find the frame {}'.format(start_frame_no))
      continue
    elif succ:
      curr_frame_no=int(line.strip().split()[frame_no_pos])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      line=file.readline()
      line=file.readline()
      line=file.readline()
      atoms=int(line[:atom_no_digits])
      bonds=int(line[atom_no_digits:2*atom_no_digits])
      for i in range(atoms):
        file.readline()
      for i in range(bonds):
        line=file.readline()
        line=processLineBonds(line)
        data['frame'].append(curr_frame_no)
        data['atom0_no'].append(line[0])
        data['atom1_no'].append(line[1])
        data['bond'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  return df
  
def getCordsAndBonds(file,start_frame_no,end_frame_no=None,atom_no_digits=3,frame_no_pos=2):
  df_cords=pd.DataFrame(columns=['frame','atom','atom_no','x','y','z'])
  df_bonds=pd.DataFrame(columns=['frame','atom0_no','atom1_no','bond'])

  if end_frame_no!=None and end_frame_no<start_frame_no:
    return (df_cords,df_bonds)

  if end_frame_no==None:
    end_frame_no=start_frame_no

  for frame_no in range(start_frame_no,end_frame_no+1):
    data_cords={'frame':[],'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
    line,succ=gotoFrame(file,frame_no,frame_no_pos=frame_no_pos)
    if not succ:
      print('Could not find the frame {}'.format(start_frame_no))
      continue
    elif succ:
      curr_frame_no=int(line.strip().split()[frame_no_pos])
      assert curr_frame_no==frame_no, 'Frame number Mismatch'
      line=file.readline()
      line=file.readline()
      line=file.readline()
      atoms=int(line.strip().split()[0])
      bonds=int(line.strip().split()[1])
      for i in range(atoms):
        line=file.readline()
        line=processLineCords(line)
        data_cords['frame'].append(curr_frame_no)
        data_cords['atom'].append(line[3])
        data_cords['atom_no'].append(i)
        data_cords['x'].append(line[0])
        data_cords['y'].append(line[1])
        data_cords['z'].append(line[2])
    tmp_df_cords=pd.DataFrame.from_dict(data_cords)
    
    data_bonds={'frame':[],'atom0_no':[],'atom1_no':[],'bond':[]}
    for i in range(bonds):
        line=file.readline()
        line=processLineBonds(line)
        data_bonds['frame'].append(curr_frame_no)
        data_bonds['atom0_no'].append(line[0])
        data_bonds['atom1_no'].append(line[1])
        data_bonds['bond'].append(line[2])
    tmp_df_bonds=pd.DataFrame.from_dict(data_bonds)
    
    df_cords=pd.concat([df_cords,tmp_df_cords],ignore_index=True)
    df_bonds=pd.concat([df_bonds,tmp_df_bonds],ignore_index=True)
  return (df_cords,df_bonds)
  
def getAdjacencyMatrix(file,start_frame_no,end_frame_no=None,atom_no_digits=3,frame_no_pos=2):
  adjacency_matrix_dict={}

  if end_frame_no!=None and end_frame_no<start_frame_no:
    return (df_cords,df_bonds)

  if end_frame_no==None:
    end_frame_no=start_frame_no

  atom_count=getAtomCount(file)
  for frame_no in range(start_frame_no,end_frame_no+1):
    bonds_df=getBonds(file,frame_no,atom_no_digits=atom_no_digits,frame_no_pos=frame_no_pos)
    adjacency_matrix=np.zeros((atom_count,atom_count))
    for index,row in bonds_df.iterrows():
      atom0=row['atom0_no']
      atom1=row['atom1_no']
      adjacency_matrix[atom0][atom1]=row['bond']
      adjacency_matrix[atom1][atom0]=row['bond']
    adjacency_matrix_dict[frame_no]=adjacency_matrix
  return adjacency_matrix_dict

def getFrameGraph(file,start_frame_no=None,end_frame_no=None,atom_no_digits=3,frame_no_pos=2):
  frame_graph_dict={}
  
  if start_frame_no==None:
    start_frame_no=0

  if end_frame_no!=None and end_frame_no<start_frame_no:
    return (df_cords,df_bonds)

  if end_frame_no==None:
    end_frame_no=start_frame_no

  atom_dict=getAtomDict(file,atom_no_digits=atom_no_digits,frame_no_pos=frame_no_pos)
  for frame_no in range(start_frame_no,end_frame_no+1):
    adjacency_matrix_dict=getAdjacencyMatrix(file,frame_no,atom_no_digits=atom_no_digits,frame_no_pos=frame_no_pos)
    G=nx.from_numpy_matrix(adjacency_matrix_dict[frame_no])
    nx.set_node_attributes(G,name='element',values=atom_dict)
    frame_graph_dict[frame_no]=G
  return frame_graph_dict
