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
total_number_of_lists, hep_hop = individual_lister(protein_chains, protein_chains_residue_numbers, hep_hop='AC_BD')

# submit the jobs to slurm
# the best way to do this, is probably to generate an sbatch-file.
# and then call a shell command to run it
name_of_sbatch_file = sbatcher(name_of_repaired)

sbatch_call = subprocess.Popen('sbatch ' + name_of_sbatch_file, stdout=subprocess.PIPE)
sbatch_process_ID_info = sbatch_call.communicate()
sbatch_process_ID = sbatch_process_ID_info.split()[4]
print('the sbatch process id is', sbatch_process_ID)

# collect scores and build a matrix
# of course this will not be possible before the sbatch
# is completely finished. The easiest way to wait for this
# is probably to submit the score collection as job to
# slurm, with a dependency (the finish of the saturation)
# it is fortunate that this is the last step, this
# makes it easy to leave as a seperate part

# put a python function call inside precedurally generated python script
srun_command = 'srun --dependency-afterany:' + sbatch_process_ID + ' somebash.sh'
subprocess.Popen(srun_command, shell=True)
#score_collect(name_of_repaired='4ins_Repair', number_of_lists=total_number_of_lists)
