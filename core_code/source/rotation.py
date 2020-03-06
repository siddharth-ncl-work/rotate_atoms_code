import math
from math import cos,sin
import numpy as np

from lib.basic_operations import vector


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


def rotateAlongAxis(cords,axis,theta,atom_list=[]):
  if len(atom_list)==0:
    atom_list=list(cords['atom_no'].values)
  new_cords=cords.copy()
  part_cords=cords[cords['atom_no'].isin(atom_list)]
  R=getRotMat(axis,theta)
  _cords=part_cords[['x','y','z']].values
  new_cords.loc[new_cords['atom_no'].isin(atom_list),['x','y','z']]=np.matmul(_cords,R.T)
  return new_cords

