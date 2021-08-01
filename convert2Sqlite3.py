#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
import numpy as np
#import skimage
#import skimage.io
#import skimage.util
from joblib import Parallel, delayed
from read_files_in_folder import read_files_in_folder


if len(sys.argv) != 3:
    sys.stdout.write('ERROR - usage: python3 conver2Sqlite3.py INPUT_GDAL_FOLDER OUTPUT_SQLITE_FOLDER \n')
    exit(0)

#print(sys.argv)
inputfolder = sys.argv[1]
outputfolder = sys.argv[2]







file_list = read_files_in_folder(inputfolder)[0]
sys.stdout.write('Processing ' + str(len(file_list)) + ' images \n')

def processInput(x):

    cwd = sys.path[0]
    cmd = 'php ' +cwd+  '/convertSqliteSingle.php '+inputfolder+' '+outputfolder+' '+file_list[x]
    sys.stdout.write(cmd+'\n')
    os.system(cmd)
    #cwd = sys.path[0]
    #sys.stdout.write(cwd+'\n')


p_tasks = 8
sys.stdout.write('Running ' + str(p_tasks) + ' parallel tasks\n')
results = Parallel(n_jobs=p_tasks)(delayed(processInput)(i) for i in range(0, len(file_list)))
