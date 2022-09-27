import gzip
from os import listdir, path
from Bio.PDB.PDBParser import PDBParser
import pandas as pd
import sys

parser = PDBParser(PERMISSIVE=1)


def process_pdb(f_in, d_f):
    """
    Take a pdb file and convert header in table
    args: 
    - <f_in> path pdb file in
    - <d_f> dict as dataframe to add header extracted 
    """

    f_in = gzip.open(f_in, 'rt')
    structure = parser.get_structure("11", file=f_in)
    f_in.close()

    # coordinate
    c_res_atom = structure.get_residues()

    #store hearder info
    d_temp = {}
    for k in structure.header.keys():
        d_temp[k] = structure.header[k]
    
    if d_f != {}:
        n_data_in = len(d_f[list(d_f.keys())[0]])
    else:
        n_data_in = 0 

    # l_inter
    l_union = list(set(list(d_temp.keys())) | set(list(d_f.keys())))
    l_inter = list(set(list(d_temp.keys())) & set(list(d_f.keys())))
    
    for k_union in l_union:
        if k_union in l_inter:
            d_f[k_union].append(d_temp[k_union])
        elif k_union in list(d_temp.keys()):
            d_f[k_union] = ["NA"] * n_data_in
            d_f[k_union].append(d_temp[k_union])
        else:
            d_f[k_union].append("NA")


## MAIN ##
##########
InDirPath = sys.argv[1]
OutFileName = sys.argv[2]



# test on the first file
l_dir = listdir(InDirPath)

dict_out = {}

for dir_pdb in l_dir[:2]:
    l_f_pdb = listdir(InDirPath + dir_pdb)
    for f_pdb in l_f_pdb:
        pf_PDB = "%s%s/%s"%(InDirPath, dir_pdb, f_pdb)
        process_pdb(pf_PDB, dict_out)


df_out = pd.DataFrame(data=dict_out)
df_out.to_parquet(OutFileName, compression='gzip')

