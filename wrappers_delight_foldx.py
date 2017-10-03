#! /usr/bin/python3.5
# This part should string all the functions together
import subprocess
from pdb_parse import pdb_parse
from individual_list_generater import individual_lister
from repair_foldx.py import repair_foldx
from score_collect.py import score_collect
from sbatch_generater.py import sbatcher
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
# and then call a shell command to run it
name_of_sbatch_file = sbatcher(name_of_repaired)

sbatch_call = subprocess.Popen('sbatch ' + name_of_sbatch_file, stdout=subprocess.PIPE)
sbatch_process_ID = sbatch_call.communicate()

print('the sbatch process id is', sbatch_process_ID)

# collect scores and build a matrix
# first determine the number of individual lists
number_of_individual_lists = 'fix this later'
all_ddgs = score_collect(name_of_repaired='4ins_Repair', number_of_lists=205)
