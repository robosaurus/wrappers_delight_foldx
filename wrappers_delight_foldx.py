#! /usr/bin/python3.5
# This part should string all the functions together
from pdb_parse import pdb_parse
from individual_list_generater import individual_lister
from repair_foldx.py import repair_foldx

# this is the path to foldx
foldx_path = '/groups/sbinlab/software/foldx_Jan17'

# first use foldX to repair the pdb
# the name of the repaired structure is saved to a variable
name_of_repaired = repair_foldx('4ins.pdb', path_to_foldx=foldx_path)
print('repairing structure and naming it ' + name_of_repaired)

# PDB_parse (including Chainselector)
protein_chains, protein_chains_residue_numbers = pdb_parse('./4ins_Repair.pdb')
for chain in protein_chains:
    print(chain, protein_chains[chain],
          protein_chains_residue_numbers[chain][0],
          protein_chains_residue_numbers[chain][-1])

# generate mutfiles (the old format!)
hep_hop = individual_lister(protein_chains, protein_chains_residue_numbers, hep_hop='AC_BD')

# submit the jobs to slurm
# the best way to do this, is probably to generate an sbatch-file.



# submit repair PDB
# just do this with subprocess



# collect scores and build a matrix
