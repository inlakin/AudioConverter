#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pickle
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

    if any(original_extension in f for f in files):
        print "[*] Found %s file(s) in '%s'" % (original_extension, rel_root)
        new_dir = create_dir(rel_root, new_extension)

    for file in files:
        if original_extension in file:
            # f     = os.path.join(rel_root, file)
            new_f = new_file_name(file, original_extension, new_extension)
            
            print "[*] Converting : '%s' into '%s/%s'" % (file, rel_root, new_f)
            
            if convert(root, new_dir, file, original_extension, new_extension, bitrate):
                file_converted += 1
            else:
                has_error = True
                error_files.append([root, file])

    print "[*] Leaving '%s'" % rel_root

print ""
print "[*] %d file(s) converted." % file_converted

# Write the audio files that were skipped in a file for logging
if has_error:
    try:
        with open(logerror_file, "a") as f:
            p = pickle.Pickler(f)
            p.dump(error_files)
        f.close()
        print "[*] Log file created :  '%s'" % logerror_file
    except Exception, e:
        print "[-] Unable to create or open the file 'fichiers_erreurs.txt"
        print "[-] Error : %s " % e

