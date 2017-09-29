#!/usr/bin/python
import os

def sbatcher(repaired_pdb, path_to_foldx='/groups/sbinlab/software/foldx_Jan17'):
    ''' as a part of foldx saturation mutagenisis, this function makes an
    sbatch file suitable for submission to slurm. It is dependent on the
    presence of a repaired PDB structure (from foldx repair pdb), and
    on the presence of a folder called individual_lists, that contains
    a bunch of mutation specifications (from the individual_list_generator)'''

    # first determine the number of jobs to submit (that is number of individual lists)
    path, dirs, files = os.walk('./individual_lists').__next__()
    number_of_files = (len(files))

    # and make a folder for the output
    if not os.path.exists('./output/'):
        os.makedirs('./output/')

    # and start making the actual sbatch file
    sbatch = open('./foldx_saturation_mutagenesis.sbatch', 'w')
    sbatch.write('''#!/bin/sh
#SBATCH --job-name=foldx_ddg_saturation
#SBATCH --array=0-{}
#SBATCH --nodes=1
#SBATCH --time=5:00:00
#SBATCH --partition=sbinlab
LST=(`ls individual_lists/individual_list*`)
OFFSET=0
INDEX=$((OFFSET+SLURM_ARRAY_TASK_ID))
echo $INDEX

# we need to determine what individual list it is using
CURRENT_LIST=(`echo ${{LST[$INDEX]}} | cut -d'/' -f 2`)
echo 'making dir output/$CURRENT_LIST'
mkdir output/$CURRENT_LIST

# and then launching foldx
{}/foldx --command=BuildModel --rotabaseLocation={}/rotabase.txt --pdb={} --mutant-file=${{LST[$INDEX]}} --numberOfRuns=1 --output-dir=output/$CURRENT_LIST
    '''.format(number_of_files, path_to_foldx, path_to_foldx, repaired_pdb))
    sbatch.close()


sbatcher('4ins_Repair.pdb')
