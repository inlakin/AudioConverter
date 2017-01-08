#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from settings import *
from functions import *
from docopt import docopt

reload(sys)
sys.setdefaultencoding('utf-8')

# # # # # # # # # # # # #
#                       #
#       Main loop       #
#                       #
# # # # # # # # # # # # #


if __name__ == '__main__':

    global original_extension
    global new_extension
    global bitrate
    global logerror_file
    global check_files
    global path_to_folder
    global new_dir
    global new_folder

    arguments = docopt(docopt_arg, version='0.1')

    if arguments["<original_codec>"] is not None:
        original_extension = arguments["<original_codec>"]
        new_extension      = arguments["--to"]
        bitrate            = arguments["--bitrate"]
        logerror_file      = arguments["--output_file"] 
        check_files        = arguments["--check"]

        if (arguments["--path"] is not None):
            path_to_folder = arguments["--path"]
        
print "Path to music folder : %s" % path_to_folder
os.chdir(path_to_folder)
path_to_folder = os.getcwd()

if check_files:
    if search_files(path_to_folder, original_extension, nb_files):
        print "Continuing"

    else:
        print "[*] Exiting."
        sys.exit(0)


for root, dirs, files in os.walk(path_to_folder):
    
    # Ignoring hidden folders/files recursively
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']

    rel_root = relative_dir_name(root)

    print ""
    print "[*] Entering '%s'" % rel_root    

    # Checking if there is any file matching our extension
    if any(original_extension in f for f in files):
        print "[*] Found %s file(s) in '%s'" % (original_extension, rel_root)
        dir_to_create = rel_root + " - " + new_extension
        
        # Checking if a directory for storing our converted files exist already
        # if it doesn't exist, we create it 
        if not os.path.isdir(dir_to_create):
            if not create_dir(dir_to_create):
                print "[-] Failed to create folder %s " % dir_to_create
                sys.exit(0)

        # If it already exist
        else:
            print "[*] Folder %s exist." % dir_to_create

            # We compare the two folders 
            # If there is the same amount of audio files in both
            if (compare_folder(rel_root, dir_to_create, original_extension, new_extension)):
                # We check the integrity of the files in our folder containing the converted audio files
                print "\t[*] Checking integrity of files"

                # If the integrity is correct, we change folder
                continue

            # if the content of the two folders is not the same we resume the conversion on the file that are missing 
            else:
                print "[*] Resuming conversion in %s " % rel_root
            
        for file in files:
            if original_extension in file:
                # f     = os.path.join(rel_root, file)
                new_f = new_file_name(file, original_extension, new_extension)
                
                print "[*] Converting : '%s' into '%s/%s'" % (file, dir_to_create, new_f)
                
                if convert(root, dir_to_create, file, original_extension, new_extension, bitrate, logerror_file):
                    file_converted += 1

    print "[*] Leaving '%s'" % rel_root

print ""
print "[*] %d file(s) converted." % file_converted
