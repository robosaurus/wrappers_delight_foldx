#!/usr/bin/python3.5

# This script will take a pdb structure and chain specifications and submit
# foldx ddg prediction jobs, to slurm, for all the residues individually substituted for
# each of the 20 amino acids. The scores will be collected in a summary file ending with .ddg
#
# the script should be called like python3 wrappers_delight_foldx.py [structure.pdb] [chains]
# The chains should be seperated into blocks seperated by underscores.
# Each block will mutate in parallel.
# For instance ABC_D, will mutate first all the residue in A and C,
# with each ddg value corresponding to three substitutions, and then afterwards
# mutate all the residues in chain D, with each ddg corresponding to
# a single aa substitution


# This part should string all the functions together

import sys
import subprocess
import random
from pdb_parse import pdb_parse
from individual_list_generater import individual_lister
from repair_foldx import repair_foldx
from sbatch_generater import sbatcher

name_of_pdb = sys.argv[1]
chainblocks = sys.argv[2]
# when calling the collect function at the end, we need to know the location
# of this folder
location_of_wrapper = sys.argv[0][0:-25]


# this is the path to foldx
foldx_path = '/groups/sbinlab/software/foldx_Jan17'

# first use foldX to repair the pdb
# the name of the repaired structure is saved to a variable
name_of_repaired = repair_foldx(name_of_pdb, path_to_foldx=foldx_path)

# PDB_parse (including Chainselector)
protein_chains, protein_chains_residue_numbers = pdb_parse(name_of_repaired)
for chain in protein_chains:
    print(chain, protein_chains[chain],
          protein_chains_residue_numbers[chain][0],
          protein_chains_residue_numbers[chain][-1])

# generate mutfiles (the old format!)
total_number_of_lists, hep_hop, residue_index_string = individual_lister(protein_chains, protein_chains_residue_numbers, hep_hop=chainblocks)

# submit the jobs to slurm
# the best way to do this, is probably to generate an sbatch-file.
# and then call a shell command to run it
name_of_sbatch_file = sbatcher(name_of_repaired)

sbatch_call = subprocess.Popen('sbatch ' + name_of_sbatch_file, stdout=subprocess.PIPE, shell=True)
# this will give us standard out from the sbatch submission
sbatch_process_ID_info = sbatch_call.communicate()
# this is where the process Id is
sbatch_process_ID = str(sbatch_process_ID_info[0]).split()[3][0:-3]
print('the sbatch process id is', sbatch_process_ID)

# collect scores and build a matrix
# of course this will not be possible before the sbatch
# is completely finished. The easiest way to wait for this
# is probably to submit the score collection as job to
# slurm, with a dependency (the finish of the saturation)
# it is fortunate that this is the last step, this
# makes it easy to leave as a seperate part

# put a python function call inside an sbatch script
# Sbatch script are good at waiting for other jobs to finish
# also since this is the last step, we will do some cleanup at the end
random_number = random.randint(1, 10000)

score_sbatch = open('./score.sbatch', 'w')
score_sbatch.write('''#!/bin/sh
#SBATCH --job-name=collect_ddgs
#SBATCH --array=1
#SBATCH --nodes=1
#SBATCH --time=0:20:00
#SBATCH --partition=sbinlab

# This sbatch script launches the score collect python function
python3 {}score_collect.py {} {} \"{}\"

# this part is for cleaning up, let's put everything in a nice tarball
tar -czf output_and_temp_files{}.tar.gz slurm* score.sbatch {} {} {}.fxout --remove-files
'''.format(location_of_wrapper, total_number_of_lists, name_of_repaired, residue_index_string, sbatch_process_ID, random_number, name_of_repaired, name_of_repaired[0:-4], name_of_sbatch_file))

score_sbatch.close()

sbatch_score_command = 'sbatch --dependency=afterany:' + sbatch_process_ID + ' score.sbatch'
subprocess.Popen(sbatch_score_command, shell=True)
