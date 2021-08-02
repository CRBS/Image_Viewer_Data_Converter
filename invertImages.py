#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
import numpy as np
#import sqlite3
from joblib import Parallel, delayed
from read_files_in_folder import read_files_in_folder


if len(sys.argv) != 3:
    sys.stdout.write('ERROR - usage: python3 invertImages.py INPUT_IMAGE_FOLDER OUTPUT_INVERTED_FOLDER \n')
    exit(0)

print(sys.argv)
inputfolder = sys.argv[1]
outputfolder = sys.argv[2]


os.mkdir(outputfolder)
file_list = read_files_in_folder(inputfolder)[0]
sys.stdout.write('Processing ' + str(len(file_list)) + ' images \n')

def processInput(x):
    file_in = os.path.join(inputfolder, file_list[x])

    file_out = os.path.join(outputfolder, file_list[x])

    cmd = 'convert '+file_in+' -channel RGB -negate '+file_out
    sys.stdout.write(cmd+'\n')
    os.system(cmd)

p_tasks = 8
sys.stdout.write('Running ' + str(p_tasks) + ' parallel tasks\n')
results = Parallel(n_jobs=p_tasks)(delayed(processInput)(i) for i in range(0, len(file_list)))
