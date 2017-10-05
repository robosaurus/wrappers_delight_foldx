#! /usr/bin/python3.5
from pdb_parse import pdb_parse
import os

def individual_lister(protein_chains, protein_chains_residue_number_list, hep_hop='A', list_length=5):
    # the hep_hop variable will group together the chains.
    # each member of a group will mutate in parralel to all
    # the other group members. (This is to mimic a situation
    # where a single mutated gene is responsible for multiple
    # protein chains)
    number_of_blocks = hep_hop.count('_') + 1
    print('the number of blocks (clustered chains) that will mutate in parallel is', number_of_blocks)
    if number_of_blocks == 1:
        hep = hep_hop
        hop = ''
        hippy = ''
    elif number_of_blocks == 2:
        hep = hep_hop.split('_')[0]
        hop = hep_hop.split('_')[1]
        hippy = ''
    elif number_of_blocks == 3:
        hep = hep_hop.split('_')[0]
        hop = hep_hop.split('_')[1]
        hippy = hep_hop.split('_')[2]
    elif number_of_blocks > 3:
        print('ERROR: too many chainblocks. You have to add bubba to the boogie support')

    print('hep is', hep)
    if hop:
        print('hop is', hop)
    if hippy:
        print('hippy is', hippy)

    # this dictionary will hold the chains as keys, and a list of mutation
    # specifications for that chain
    mutation_dictionary = {}

    # Here is a string with all the AAs, by single letter-code
    all_AAs = 'ACDEFGHIKLMNPQRSTVWY'

    for chain in protein_chains:
        mutation_dictionary[chain] = []
        # this is the entry currently being considered
        entry = 0
        for residue in protein_chains[chain]:
            for mutate_to in all_AAs:
                mutation_spec = residue + chain + protein_chains_residue_number_list[chain][entry] + mutate_to
                mutation_dictionary[chain].append(mutation_spec)
            entry += 1

    for chain in mutation_dictionary:
        print(chain, len(mutation_dictionary[chain]))

    # and now for the writing of the actual individual_lists
    # an important variable sets the size of the individual lists
    list_length = list_length
    # and the following variable keeps track of when we reach the max
    current_list_size = 0
    # and here is one to hold the number of list we have reached
    current_list_number = 1
    # we put all the lists in a folder
    # first let us check if it already exists, otherwise create it
    if not os.path.exists('./individual_lists/'):
        os.makedirs('./individual_lists/')
    # and we open the first list
    individual_list = open('./individual_lists/individual_list'+str(current_list_number)+'.txt', 'w')

    # consider first the hep
    # and this will keep track of what mutation_spec has been reached
    mutation_spec_number = 0
    for mutation_spec in mutation_dictionary[hep[0]]:
        # first off, the line will contain at least one mutation
        # that is the mutation specified by the first chain in hep
        list_line = mutation_spec
        # and then, if there are more chains in hep, the corresponding
        # mutation for that chain should be added
        for chain in hep:
            if chain != hep[0]:
                list_line += ',' + mutation_dictionary[chain][mutation_spec_number]
        # and increment the counter, to make sure the chains
        # follow the same pace
        mutation_spec_number += 1
        # write and close the line
        individual_list.write(list_line + ';\n')
        # and we increment the list_size_variable
        current_list_size += 1
        # and check if we need to move on
        if current_list_size >= list_length:
            individual_list.close()
            current_list_number += 1
            individual_list = open('./individual_lists/individual_list'+str(current_list_number)+'.txt', 'w')
            # and reset the counter
            current_list_size = 0

    # and we do the same thing for hop (if it exists)
    if hop:
        mutation_spec_number = 0
        for mutation_spec in mutation_dictionary[hop[0]]:
            # first off the line will contain at least one mutation
            list_line = mutation_spec
            # and then, if there are more chains in hep, the corresponding
            # mutation for that chain should be added
            for chain in hop:
                if chain != hop[0]:
                    list_line += ',' + mutation_dictionary[chain][mutation_spec_number]
            # that is end of the line. So increment the counter,
            # to make sure the chains follow the same pace
            mutation_spec_number += 1
            # write and close the line
            individual_list.write(list_line + ';\n')
            # and we increment the list_size_variable
            current_list_size += 1
            # and check if we need to move on
            if current_list_size >= list_length:
                individual_list.close()
                current_list_number += 1
                individual_list = open('./individual_lists/individual_list'+str(current_list_number)+'.txt', 'w')
                # and reset the counter
                current_list_size = 0

    # and while we are at it lets add hippy support. If someone really needs it
    # feel free to add bubba to the bang bang boogie support later.
    if hippy:
        mutation_spec_number = 0
        for mutation_spec in mutation_dictionary[hippy[0]]:
            # first off the line will contain at least one mutation
            list_line = mutation_spec
            # and then, if there are more chains in hep, the corresponding
            # mutation for that chain should be added
            for chain in hippy:
                if chain != hippy[0]:
                    list_line += ',' + mutation_dictionary[chain][mutation_spec_number]
            # that is end of the line. So increment the counter,
            # to make sure the chains follow the same pace
            mutation_spec_number += 1
            # write and close the line
            individual_list.write(list_line + ';\n')

            # and we increment the list_size_variable
            current_list_size += 1
            # and check if we need to move on
            if current_list_size >= list_length:
                individual_list.close()
                current_list_number += 1
                individual_list = open('./individual_lists/individual_list'+str(current_list_number)+'.txt', 'w')
                # and reset the counter
                current_list_size = 0

    individual_list.close()
    # make a dictionary that informs score_collect.py of the indices and chains relations
    # this dictionary will have a block as key, and a residue length as value
    residue_index_chain_dictionary = {}
    block_index_start = 1
    block_index_end = 0
    for block in hep_hop.split('_'):
        block_index_end = block_index_start + len(mutation_dictionary[block[0]]) / 20
        residue_index_chain_dictionary[block] = '{} to {}'.format(block_index_start, block_index_end)
        block_index_start = block_index_end

    # return the number of total number of lists, and hep_hop (chain scheme)
    # and the residue_index_chain_dictionary (for score_collect).
    return current_list_number, hep_hop, residue_index_chain_dictionary
