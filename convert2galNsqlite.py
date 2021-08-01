#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
import numpy as np
import sqlite3
from joblib import Parallel, delayed
from read_files_in_folder import read_files_in_folder


if len(sys.argv) != 4:
    sys.stdout.write('ERROR - usage: python3 conver2galNsqlite.py INPUT_IMAGE_FOLDER OUTPUT_GDAL_FOLDER OUTPUT_SQLITE_FOLDER \n')
    exit(0)

print(sys.argv)
inputfolder = sys.argv[1]
outputfolder = sys.argv[2]
sql_folder = sys.argv[3]


os.mkdir(outputfolder)
file_list = read_files_in_folder(inputfolder)[0]
sys.stdout.write('Processing ' + str(len(file_list)) + ' images \n')

def processInput(x):
    file_in = os.path.join(inputfolder, file_list[x])
    #sys.stdout.write('Loading: ' + str(file_in) + '\n')

    nameArray = file_list[x].split('.');
    iname = str(int(nameArray[1]))

    file_out = os.path.join(outputfolder, iname)
    #sys.stdout.write('Saving: ' + str(file_out) + '\n')

    cmd = 'gdal2tiles.py -p raster '+file_in+' '+file_out
    sys.stdout.write(cmd+'\n')
    os.system(cmd)


    cwd = sys.path[0]
    cmd = 'php ' +cwd+  '/convertSqliteSingle.php '+outputfolder+' '+sql_folder+' '+iname
    sys.stdout.write(cmd+'\n')
    os.system(cmd)

p_tasks = 8
sys.stdout.write('Running ' + str(p_tasks) + ' parallel tasks\n')
results = Parallel(n_jobs=p_tasks)(delayed(processInput)(i) for i in range(0, len(file_list)))
