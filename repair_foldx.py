#!/usr/bin.python3.5
import subprocess

def repair_foldx(pdb_name, path_to_foldx='/groups/sbinlab/software/foldx_May18/'):
    foldx_path = path_to_foldx
    # let us put the subprocess call in a string
    # watch the spaces!
    the_call = ('srun '
                + foldx_path
                + '/foldx -c RepairPDB --pdb=' + pdb_name
                + ' --rotabaseLocation=' + foldx_path + '/rotabase.txt'
                + ' &> repairlog.log')

    print('calling to the shell:')
    print(the_call)
    # this is the shell command for srunning foldx repair pdb
    print('\n repairing... this is going to take some minutes')
    srun_process = subprocess.Popen(the_call, shell=True)
    # wait for it to finish, we need the repair to continue
    srun_process.communicate()

    name_of_repaired = pdb_name[0:-4] + '_Repair.pdb'
    print('the name of the repaired pdb is ', name_of_repaired)
    return(name_of_repaired)
