
def writeCords(file_path,df):
  file=open(file_path,'w')
  atoms=df.shape[0]
  file.write(str(atoms)+'\n\n')
  for i in range(atoms):
    row=df.iloc[i,:]
    line=row['atom']+'  '+ \
         str(row['x'])+'  '+ \
         str(row['y'])+'  '+ \
         str(row['z'])+'\n'
    file.write(line)
  file.close()

def fixAtoms(file_path,df,atoms_list):
  file=open(file_path,'w')
  atoms=df.shape[0]
  file.write(str('$coord\n'))
  for i in range(atoms):
    row=df.iloc[i,:]
    line=str(row['x'])+'  '+ \
         str(row['y'])+'  '+ \
         str(row['z'])+'  '+ \
         str(row['atom'])+'  '
    if i in atoms_list:
      line+='f\n'
    else:
      line+='\n'
    file.write(line)
  file.write('$user-defined bonds\n$end')
  file.close()
   
