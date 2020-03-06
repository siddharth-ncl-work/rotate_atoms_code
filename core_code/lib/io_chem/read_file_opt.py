import pandas as pd

def totalAtoms(file_path):
  file=open(file_path,'r')
  line=file.readline()
  atoms=0
  while line!='':
    line=file.readline()
    if '$' in line:
      break
    atoms+=1
  file.close()
  return atoms

def processLineCords(line):
  line=line.strip().split()
  line=line[:4]
  line[0]=float(line[0])
  line[1]=float(line[1])
  line[2]=float(line[2])
  return line

def getCords(file_path):
  data={'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
  atoms=totalAtoms(file_path)
  file=open(file_path,'r')
  line=file.readline() 
  for i in range(atoms):
    line=file.readline()
    line=processLineCords(line)
    data['atom'].append(line[3])
    data['atom_no'].append(i)
    data['x'].append(line[0])
    data['y'].append(line[1])
    data['z'].append(line[2])
  df=pd.DataFrame.from_dict(data)
  return df

