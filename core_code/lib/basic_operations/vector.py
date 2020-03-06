import numpy as np

def getMag(v):
  return np.linalg.norm(v)

def getUnitVec(v):
  if getMag(v)==0:
    return [0,0,0]
  return v/getMag(v)

def getDotProduct(v1,v2):
  return np.dot(v1,v2)

def getCrossProduct(v1,v2):
  return np.cross(v1,v2)

def getAngleD(v1,v2):
  theta=math.acos(np.dot(v1,v2)/(getMag(v1)*getMag(v2)))
  return math.degrees(theta)

def getAngleR(v1,v2):
  v=np.dot(v1,v2)/(getMag(v1)*getMag(v2))
  if v>1:
    v=1
  elif v<-1:
    v=-1
  return np.arccos(v)

def get_dist_pt_line(point,line_vec):
  theta=getAngleR(point,line_vec)
  mag=getMag(point)
  return mag*np.sin(theta)

def getDihedralAngle(p,unit='radians'):
    """Praxeolitic formula \
    1 sqrt, 1 cross product"""
    p0 = p[0]
    p1 = p[1]
    p2 = p[2]
    p3 = p[3]

    b0 = -1.0*(p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2

    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 /= np.linalg.norm(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - np.dot(b0, b1)*b1
    w = b2 - np.dot(b2, b1)*b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)
    theta=np.arctan2(y, x)
    if unit=='radians':
      return theta
    elif unit=='degrees':
      np.degrees(theta)

def getPlaneNormal(atoms_array):
  if atoms_array.shape!=(3,3):
    print('please check atoms array')
    return
  v1=atoms_array[0]-atoms_array[1]
  v2=atoms_array[2]-atoms_array[1]
  normal=getCrossProduct(v1,v2)
  return getUnitVec(normal)

def getProjection(v1,v2):
  return getDotProduct(v1,v2)/getMag(v2)

if __name__=='__main__':
  '''
  from lib.io_chem import io
  file_path='benzene.xyz'
  df=io.readFile(file_path)
  print(df) 
  p=df[df['atom_no'].isin([10,4,5,11])][['x','y','z']].values
  print(getDihedralAngle(p))
  p=df[df['atom_no'].isin([8,2,5,11])][['x','y','z']].values
  print(getDihedralAngle(p))
  p=df[df['atom_no'].isin([6,0,5,11])][['x','y','z']].values
  print(getDihedralAngle(p))
  #0.000057       80.537678      116.565051     -116.565051      -45.000000
  p1 = np.array([
                [ 1,           0,         0     ],
                [ 0,           0,         0     ],
                [ 0,           0,         1     ],
                [ 0.999999,    0.000001,  1     ]
                ])

  # +x,+y
  p2 = np.array([
                [ 1,           0,         0     ],
                [ 0,           0,         0     ],
                [ 0,           0,         1     ],
                [ 0.1,         0.6,       1     ]
                ])

  # -x,+y
  p3 = np.array([
                [ 1,           0,         0     ],
                [ 0,           0,         0     ],
                [ 0,           0,         1     ],
                [-0.3,         0.6,       1     ]
                ])
  # -x,-y
  p4 = np.array([
                [ 1,           0,         0     ],
                [ 0,           0,         0     ],
                [ 0,           0,         1     ],
                [-0.3,        -0.6,       1     ]
                ])
  # +x,-y
  p5 = np.array([
                [ 1,           0,         0     ],
                [ 0,           0,         0     ],
                [ 0,           0,         1     ],
                [ 0.6,        -0.6,       1     ]
                ])
  print(getDihedralAngle(p1))
  print(getDihedralAngle(p2))
  print(getDihedralAngle(p3))
  print(getDihedralAngle(p4))
  print(getDihedralAngle(p5))
  '''
  v1=np.array([1.0,3,-2])
  v2=np.array([-2.0,4,-1])
  p=getProjection(v1,v2)
  print(p)
