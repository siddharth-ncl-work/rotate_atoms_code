import pandas as pd

def totalAtoms(file_path):
  file=open(file_path,'r')
  line=file.readline()
  atoms=int(line.strip())
  file.close()
  return atoms


def processLineCords(line):
  line=line.strip().split()
  line=line[:4]
  line[1]=float(line[1])
  line[2]=float(line[2])
  line[3]=float(line[3])
  return line


def getCords(file_path):
  data={'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}
  file=open(file_path,'r')
  atoms=int(file.readline().strip())
  file.readline()
  for i in range(atoms):
    line=file.readline()
    line=processLineCords(line)
    data['atom'].append(line[0])
    data['atom_no'].append(i)
    data['x'].append(line[1])
    data['y'].append(line[2])
    data['z'].append(line[3])
  df=pd.DataFrame.from_dict(data) 
  file.close()
  return df
