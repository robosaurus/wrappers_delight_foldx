#!/usr/bin/python3
import sys

# this function is part of wrappers_delight for foldx
# i am going to put some things here in the beginning, so you can call it from the shell
number_of_listos = int(sys.argv[1])
name_of_repairod = sys.argv[2]
index_strong = sys.argv[3]

def score_collect(number_of_lists, index_string=None, name_of_repaired='4ins_Repair', path_to_output='./output/'):
    """this is a function for looping through the output folder and collect all the ddg scores
     it returns a list, of all the ddgs"""

    # this is the list that will hold all of the ddgs
    all_ddg_scores = []
    for list_number in range(1, number_of_lists):
        # each folder will contain the results for a number of runs
        print(list_number)
        mut_number = 1
        path_to_list = path_to_output+'individual_list'+str(list_number)+'.txt'+'/Average_'+name_of_repaired[0:-4]+'.fxout'
        print(path_to_list)
        try:
            average_fxout = open(path_to_list)
        # sometimes the last list will be empty and there will not be any output in the folder
        # This exception lets us ignore the last folder (list), in that case
        except FileNotFoundError:
            print('file_not_found!! for list ', list_number)
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
                # This is a line with scores. Sussing out which mutation this
                # is a little tricky. I think it will be easiest to add the
                # scores to one long list, and then using the same
                # (but opposite) scheme that was used for individual list
                # generation, to figure out which mutations are where
                score_fields = line.split()
                ddg = score_fields[2]
                # since files are read from the top, and the range is specified
                # as from 1 to whatever, the ddgs will be read sequentially
                # and we can simply append it to the list of all_ddgs
                all_ddg_scores.append(float(ddg))

    print(len(all_ddg_scores))
    # the total number of residues is the length of the all ddgs list,
    # divided by 20, saturation remember :>
    number_of_residues = int(len(all_ddg_scores)/20)
    print('number of residues is', number_of_residues)
    # now we build the output matrix
    matrix_file = open('./ddgs_' + name_of_repaired+ '.ddg', 'w')
    # First let us write a header. That should contain the name of the structure
    matrix_file.write('# foldx ddg predictions on structure ' + name_of_repaired + '\n')
    # and a key for intrepreting the residue indices. This will use the residue_dictionary
    if index_string:
        matrix_file.write('# residue index key:\n')
        matrix_file.write(index_string)
    # and lastly of course the title on the coloumns.
    header_line = 'index'
    for element in 'ACDEFGHIKLMNPQRSTVWY':
        header_line = header_line + '\t' + element
    header_line += '\n'
    matrix_file.write(header_line)

    # this is AA number, and it will run throught the same list as we used during
    # individual list generation
    ddg_line = '{:.4f}\t'*20 + '\n'
    for residuenumber in range(1, number_of_residues):
        start_index = (residuenumber * 20) - 20
        end_index = (residuenumber*20)
        matrix_file.write(str(residuenumber) + '\t' + ddg_line.format(*all_ddg_scores[start_index:end_index]))

    matrix_file.close()

score_collect(number_of_lists=number_of_listos, name_of_repaired=name_of_repairod, index_string=index_strong)
