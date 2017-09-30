#!/usr/bin/python3

# this function is part of wrappers_delight for foldx

def score_collect(name_of_repaired=''path_to_output='./output', muts_per_list=5):
    for list_number in range(1,206):
        average_fxout = open(path_to_output+'individual_list'+list+'/Average_'+name_of_repaired+'fxout')
        average_fxout_data = average_fxout.readlines()
        average_fxout.close()

