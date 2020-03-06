# io_chem
Module to handle all i/o operations for the files used in computational chemistry
### Currently Supports following file formats:
1. mol/SDF
2. xyz
3. opt (optimization file from the cluster job)

### File Handling:
1. Small: With file path
2. Large: With file pointer

## Design rules:
* return type: Pandas Dataframe(Default)  wherever applicable
* column names: singular
* Functions: Camel case
* variables: underscores
* strings/file_name: lower case with underscore

Add Wraper to handle slightly different versions of the same file type
