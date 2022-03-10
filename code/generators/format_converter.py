###############################################################################
# File: format_converter.py
# Author: Carlos Bobed
# Date: Mar 2022
# Comments: Program to transform a .dat file into the format that tx-means handles
# Modifications:
# Notes:
##############################################################################

import argparse

def transform_data_to_synthetic(file_orig, file_out):
    with open(file_orig,'r') as in_cls, open(file_out, 'w') as  out:
        cls = list()
        id = 0
        for l in in_cls:
            out.write(str(id)+';0;'+l)
            id += 1

if __name__ == '__main__':

    # params: -input file
    #         -output file
    my_parser = argparse.ArgumentParser(allow_abbrev=False)

    my_parser.add_argument('-input', action='store', required=True,
                           help=".dat file to be converted")
    my_parser.add_argument('-output', action='store', required=False,
                           help="filename of the converted file, default: ${input/.dat/.csv}")
    args = my_parser.parse_args()

    if args.output is not None:
        output_file = args.output
    else:
        output_file = args.input[:args.input.rfind(".dat")]+".csv"

    transform_data_to_synthetic(args.input, output_file)