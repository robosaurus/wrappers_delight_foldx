#!/usr/bin/python3


def read_ddg_output(path_to_output, length_of_protein):
    # This is a function for reading the output of all the foldx ddg
    # calculations. It assumes the mutant files have been specified
    # by the individual_lister function

    number_of_lists = length_of_protein * 20 / 5

    for list_number in (1, number_of_lists):
        output_file = open('output/individual_list'+list_number+'.txt', 'r')
        output_data = output_file.readlines()
        output_file.close()

        for line in output_data:
            print line


read_ddg_output('some_path', 100)
