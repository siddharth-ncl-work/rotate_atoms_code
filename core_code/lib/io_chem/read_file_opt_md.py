import pandas as pd

def totalAtoms(file):
  file.seek(0)
  atoms=int(file.readline().strip())
  return atoms

def processLineCords(line):
  line=line.strip().split()
  line=line[:4]
  line[1]=float(line[1])
  line[2]=float(line[2])
  line[3]=float(line[3])
  return line

'''
def processEnergy(line):
  line=line.strip().split()
  line=line[:3]
  line=map(int,line)
  line[0]-=1
  line[1]-=1
  return line
'''

def totalFrames(file):
  file.seek(0)
  counter=0
  line=file.readline()
  while line!='':
    if 'energy' in line.lower():
      counter+=1
    line=file.readline()
  file.seek(0)
  return counter

def getLastFrameCords(file):
  data={'frame':[],'energy':[],'atom':[],'atom_no':[],'x':[],'y':[],'z':[]}

  file.seek(0)
  line='a'
  frame_no=0
  while line!='':
      line=file.readline()
      atoms=int(line.strip().split()[0])
      line=file.readline()
      energy=float(line.split('=')[1].strip())
      data['frame']=[]
      data['energy']=[]
      data['x']=[]
      data['y']=[]
      data['z']=[]
      for i in range(atoms):
        line=file.readline()
        line=processLine(line)
        data['frame'].append(frame_no)
        data['energy'].append(energy)
        data['atom'].append(line[3])
        data['atom_no'].append(i)
        data['x'].append(line[0])
        data['y'].append(line[1])
        data['z'].append(line[2])
      frame_no+=1
  df=pd.DataFrame.from_dict(data)
  return df

