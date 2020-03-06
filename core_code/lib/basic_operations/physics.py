from math import cos,sin
import numpy as np

from . import vector
from . import atomic_mass
from . import constants


def getMI(atom_cords,atom_type,axis):
  distance=vector.getMag(atom_cords)
  return _getMI([atom_cords],[atomic_mass.atomic_mass_dict[atom_type.lower()]],axis)  

def _getMI(cords_list,mass_list,axis):
  MI=0
  mr_list=zip(mass_list,cords_list)
  for m,cords in mr_list:
    r=vector.get_dist_pt_line(cords,axis)
    MI+=m*pow(r,2)
  return MI*constants.amu*pow(constants.angstrom,2)

def getCom(cords,atom_list=None):
  mass_list=[]
  cords_list=[]
  if atom_list==None:
    atom_list=list(cords['atom_no'].values) 
  for atom_no in atom_list:
    mass=atomic_mass.atomic_mass_dict[cords[cords['atom_no']==atom_no]['atom'].values[0].lower()]
    mass_list.append(mass)
    cords_list.append(cords[cords['atom_no']==atom_no][['x','y','z']].values[0])
  return _getCom(cords_list,mass_list)

def _getCom(cords_list,mass_list):
  com=[0.0,0.0,0.0]
  mr_list=zip(mass_list,cords_list)
  for m,r in mr_list:
    com[0]+=m*r[0]
    com[1]+=m*r[1]
    com[2]+=m*r[2]
  total_mass=np.sum(mass_list)
  com[0]/=total_mass
  com[1]/=total_mass
  com[2]/=total_mass
  return com

def getTotalMass(cords,atom_list=None):
  total_mass=0
  if atom_list==None:
    atom_list=list(cords['atom_no'].values)
  for atom_no in atom_list:
    mass=atomic_mass.atomic_mass_dict[cords[cords['atom_no']==atom_no]['atom'].values[0].lower()]
    total_mass+=mass
  return total_mass*constants.amu

def getRotMat(axis,theta):
  R=np.zeros((3,3))
  s=vector.getUnitVec(axis)
  t=theta
  vv=(1-cos(t))
  R[0][0]=s[0]*s[0]*vv+cos(t)
  R[0][1]=s[0]*s[1]*vv-s[2]*sin(t)
  R[0][2]=s[0]*s[2]*vv+s[1]*sin(t)
  R[1][0]=s[0]*s[1]*vv+s[2]*sin(t)
  R[1][1]=s[1]*s[1]*vv+cos(t)
  R[1][2]=s[1]*s[2]*vv-s[0]*sin(t)
  R[2][0]=s[0]*s[2]*vv-s[1]*sin(t)
  R[2][1]=s[1]*s[2]*vv+s[0]*sin(t)
  R[2][2]=s[2]*s[2]*vv+cos(t)
  return R

def rotateAlongAxis(cords,axis,theta):
  new_cords=cords.copy()
  R=getRotMat(axis,theta)
  _cords=cords[['x','y','z']].values
  new_cords[['x','y','z']]=np.matmul(_cords,R.T)
  return new_cords

def translateAlongAxis(cords,axis,distance):
  new_cords=cords.copy()
  _axis=vector.getUnitVec(axis)
  translation_vector=[0,0,0]
  translation_vector[0]=distance*_axis[0]
  translation_vector[1]=distance*_axis[1]
  translation_vector[2]=distance*_axis[2]
  new_cords['x']=new_cords['x']+translation_vector[0]
  new_cords['y']=new_cords['y']+translation_vector[1]
  new_cords['z']=new_cords['z']+translation_vector[2]
  return new_cords

def getCog(cords,atom_list=None):
  if atom_list==None:
    return[cords['x'].mean(),cords['y'].mean(),cords['z'].mean()]
  else:
    part_df=cords[cords['atom_no'].isin(atom_list)]
    return [part_df['x'].mean(),part_df['y'].mean(),part_df['z'].mean()]

