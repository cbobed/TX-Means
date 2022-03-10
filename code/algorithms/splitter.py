###############################################################################
# File: splitter.py
# Author: Carlos Bobed
# Date: Mar 2022
# Comments: program that applies the selected algorithm to the file that has
#   been passed as input - Adapted from original TX-means code
# Modifications:
# Notes: To begin with, it will use the default configuration parameters
#       for ALL algorithms (no fine tuning for any of them)
##############################################################################

#### Lib handling
import os, sys, importlib
from os.path import expanduser
from pathlib import Path

home = str(Path.home())
path_to_lib = os.path.join(Path.home(), 'workingDir', 'git', 'TX-Means')
print("+++"+path_to_lib)

if os.path.isdir(path_to_lib):
    print(f'My Home is: {home}')
    print(f'I cloned in: {path_to_lib}')
    # Add dirs to Python Path
    sys.path.insert(0, os.path.join(path_to_lib, 'code'))
    sys.path.insert(0, os.path.join(path_to_lib, 'code', 'algorithms'))
else:
    print("Can't find Directory.")
    print('For example: you are in')
    print(str(os.getcwd()))
#### End lib handling

import argparse
import algorithms.txmeans
from algorithms.txmeans import TXmeans
from algorithms.txmeans import remap_items, count_items, sample_size # Util functions
from algorithms.txmeans import basket_list_to_bitarray, basket_bitarray_to_list # Converting(Reverting) to(from) bitarray
from generators.datamanager import read_synthetic_data # (Convert the data in nice basket format)
from validation.validation_measures import delta_k, purity, normalized_mutual_info_score # Measure of Validation
from algorithms.util import jaccard_bitarray

import pandas as pd
import numpy as np
import IPython.display as ipd
import datetime

if __name__ == '__main__':
    # params: -input file
    my_parser = argparse.ArgumentParser(allow_abbrev=False)

    my_parser.add_argument('-input', action='store', required=True,
                           help=".dat file to be converted")
    args = my_parser.parse_args()

    txmeans_model = TXmeans()
    class_index = -1
    baskets_real_labels = read_synthetic_data(args.input)

    # Save baskets and the real labels
    baskets_list = list()
    real_labels = list()
    count = 0
    for basket, label in baskets_real_labels:
        baskets_list.append(basket)
        real_labels.append(label)
        count += 1

    # Speeding up the Jaccard distance:
    baskets_list, map_newitem_item, map_item_newitem = remap_items(baskets_list)
    baskets_list = basket_list_to_bitarray(baskets_list, len(map_newitem_item))

    # Get the number of baskets (equal to number of data)
    nbaskets = len(baskets_list)

    # Get the number of different item
    nitems = count_items(baskets_list)

    start_time = datetime.datetime.now()

    # Get subsamples of the dataset (in order to speed up)
    nsample = sample_size(nbaskets, 0.05, conf_level=0.99, prob=0.5)

    # Fit the model
    txmeans_model.fit(baskets_list, nbaskets, nitems)

    end_time = datetime.datetime.now()
    running_time = end_time - start_time

    print(f'Execution time: {running_time}')

    # Get the label and the clusters
    res = txmeans_model.clustering

    # Number of iteration of the model for the convergence
    iter_count = txmeans_model.iter_count

    # Initialize empty cluster list
    baskets_clusters = list()
    for label, cluster in enumerate(res):
        # Revert the bitarray transform.
        cluster_list = basket_bitarray_to_list(cluster['cluster']).values()
        output_file = args.input[:args.input.rfind(".dat")] + "-txmeans-"+str(label)+".dat"
        with open(output_file, 'w') as out:
            for trans in cluster_list:
                out.write(' '.join([str(elem) for elem in trans])+"\n")

