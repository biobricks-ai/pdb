import gzip
import xml.etree.ElementTree as ET
import shutil
from os import listdir, path
from Bio.PDB.PDBParser import PDBParser
import pandas as pd


parser = PDBParser(PERMISSIVE=1)


def process_pdb(f_in, d_f):

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



## MAIN
p_dir_PDB = "/mnt/md0/biobricks/pdb/download/"

# test on the first file
l_dirPDB = listdir(p_dir_PDB)

d_f = {}
count = 0
for dirpdb in l_dirPDB[:10]:
    l_filepdb = listdir(p_dir_PDB + dirpdb)
    for f_pdb in l_filepdb:
        pf_PDB = p_dir_PDB + dirpdb + "/" + f_pdb
        count = count + 1
        process_pdb(pf_PDB, d_f)

print(count)
#print(d_f)
df_out = pd.DataFrame(data=d_f)

#write in csv
p_out = "./test.csv"
df_out.to_csv(p_out)

