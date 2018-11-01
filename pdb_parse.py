#! /usr/bin/env python3
import sys

def pdb_parse(path_to_pdb):
    # this is the PDB parse function. It should take a PDB file as input
    # and determine how many chains, what they are called, and which residues they
    # span and maybe even which chains are identical

    pdb_file = open(path_to_pdb, 'r')
    pdblines = pdb_file.readlines()
    pdb_file.close()

    # This dictionary will all the  hold all the residues
    # each chain wil be a key, and the value will be the residue sequence
    protein_chains = {}
    # and this dict will have all the corresponding residue numbers
    protein_chains_residue_number_list = {}

    # these variables hold some information about the atom
    chainspec = 'NULL'
    residue_number = 'NULL'

    # this dictionary is just for translating from 3-letter codes
    # to 1-letter code

    aminocodes = {
        "ALA": "A",
        "CYS": "C",
        "ASP": "D",
        "GLU": "E",
        "PHE": "F",
        "GLY": "G",
        "HIS": "H",
        "ILE": "I",
        "LYS": "K",
        "LEU": "L",
        "MET": "M",
        "ASN": "N",
        "PRO": "P",
        "GLN": "Q",
        "ARG": "R",
        "SER": "S",
        "THR": "T",
        "VAL": "V",
        "TRP": "W",
        "TYR": "Y"
    }

    for line in pdblines:
        # this just removes empty lines
        if len(line) > 1:
            line_fields = line.split()
            if line_fields[0] == 'ATOM':
                entry_type = line_fields[0]
                atom_number = line_fields[1]
                atom_type = line_fields[2]
                # pdbs have AA three letter codes, let us
                # translate that to single letter
                residue_type = line[17:20]
                residue_letter = aminocodes[residue_type]

                # the chainspecification always happens at the
                # 22nd character of the line. It is not always
                # seperated by spaces. And some pdbs use the
                # legacy <space> instead of a letter, if there
                # is only one chain
                previous_chainspec = chainspec
                chainspec = line[21]
                # since there is not always room for a space
                # in the pdb, we have to get a little creative
                # with how we select the residue index
                previous_residue_number = residue_number
                residue_number = line[22:26]
                # and remove the whitespace
                residue_number = residue_number.lstrip()
                # check to see if the residue is a new one
                if residue_number != previous_residue_number or chainspec != previous_chainspec:
                    if chainspec in protein_chains:
                        protein_chains[chainspec] += residue_letter
                        protein_chains_residue_number_list[chainspec] += [
                            residue_number
                        ]
                    else:
                        protein_chains[chainspec] = residue_letter
                        protein_chains_residue_number_list[chainspec] = [
                            residue_number
                        ]
    # and add the last residue!
    if residue_number != previous_residue_number or chainspec != previous_chainspec:
        if chainspec in protein_chains:
            protein_chains[chainspec] += residue_letter
            protein_chains_residue_number_list[chainspec] += [
                residue_number
            ]
        else:
            protein_chains[chainspec] = residue_letter
            protein_chains_residue_number_list[chainspec] = [
                residue_number
            ]

    return protein_chains, protein_chains_residue_number_list


# this last part is just so you can call it from the shell
if __name__ == '__main__':
    prochains, reslist = pdb_parse(sys.argv[1])
    print(prochains)
