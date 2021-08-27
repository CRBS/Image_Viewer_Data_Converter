import sys
import os

from read_files_in_folder import read_files_in_folder

if len(sys.argv) != 3:
    sys.stdout.write('ERROR - usage: python3 copyFolderToServer.py INPUT_FOLDER REMOTE_FOLDER \n')
    exit(0)


serverName = input("ENter host name: ")
auth = input("Enther authentication information: ")


inputfolder = sys.argv[1]
outputfolder = sys.argv[2]

file_list = read_files_in_folder(inputfolder)[0]

for file in file_list:
    file_in = os.path.join(inputfolder, file)
    #file_in = inputfolder+"/"+file
    
    if(os.path.isfile(file_in)):

        upload_url = "https://"+serverName+"/CIL-Storage-RS/index.php/External_file_upload/upload_orig_file/"+outputfolder
        cmd = "curl -u "+auth+" -F 'data=@"+file_in+"' "+upload_url
        os.system(cmd)
        #print (cmd)
