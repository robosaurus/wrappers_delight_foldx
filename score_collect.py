#!/usr/bin/python3

# this function is part of wrappers_delight for foldx

def score_collect(name_of_repaired='4ins_Repair', path_to_output='./output/', number_of_lists):
    """ this is a function for looping through the output folder and collect all the ddg scores
     it returns a list, of all the ddgs"""

    # this is the list that will hold all of the ddgs
    all_ddg_scores = []
    for list_number in range(1, number_of_lists):
        # each folder will contain the results for a number of runs
        mut_number = 1
        path_to_list = path_to_output+'individual_list'+str(list_number)+'.txt'+'/Average_'+name_of_repaired+'_'+'.fxout'
        try:
            average_fxout = open(path_to_output+'individual_list'+str(list_number)+'.txt'+'/Average_'+name_of_repaired+'.fxout')
        # sometimes the last list will be empty and there will not be any output in the folder
        # This exception lets us ignore the last folder (list), in that case
        except FileNotFoundError:
            continue

        average_fxout_data = average_fxout.readlines()
        average_fxout.close()
        print(list_number)
        # this variable will keep track of what line number we are reading
        output_line_number = 0
        for line in average_fxout_data:
            output_line_number += 1
            # the first 9 lines do not contain any data
            if output_line_number < 10:
                # do not do anything
                continue
            else:
                # This is a line with scores. Sussing out which mutation this is
                # is a little tricky. I think it will be easiest to add the scores
                # to one long list, and then using the same (but opposite) scheme that was used for
                # individual list generation, to figure out which mutations are where
                score_fields = line.split()
                ddg = score_fields[2]
                # since files are read from the top, and the range is specified
                # as from 1 to whatever, the ddgs will be read sequentially
                # and we can simply append it to the list of all_ddgs
                all_ddg_scores.append(ddg)

    return all_ddg_scores

score_collect()
