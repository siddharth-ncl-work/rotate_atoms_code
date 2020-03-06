import pandas as pd
from tqdm import tqdm

def totalAtoms(file):
  with open(file.name,'r') as _file:
    atoms=int(_file.readline())
  return atoms

def gotoFrame(file,frame_no,frame_no_pos=1):
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
  line[0]=line[0].strip()
  line[1]=float(line[1])
  line[2]=float(line[2])
  line[3]=float(line[3])
  return line

def getCords(file,start_frame_no,end_frame_no=None,frame_no_pos=1,atoms=-1):
  data={'frame':[],'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
 
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
      atoms=totalAtoms(file)      
      for i in range(atoms):
        line=file.readline()
        line=processLineCords(line)
        data['frame'].append(curr_frame_no)
        data['atom'].append(line[0])
        data['atom_no'].append(i)
        data['x'].append(line[1])
        data['y'].append(line[2])
        data['z'].append(line[3])
  df=pd.DataFrame.from_dict(data)
  return df

  
