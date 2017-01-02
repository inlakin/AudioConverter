#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pickle

from functions import *

# # # # # # # # # # # # #
#                       #
#       Main loop       #
#                       #
# # # # # # # # # # # # #

path = os.getcwd()

if search_files(path):

    for root, dirs, files in os.walk(path):
        # files = [f for f in files if not f[0] == '.']
        # dirs[:] = [d for d in dirs if not d[0] == '.']
        rel_root = relative_dir_name(root)
        
        print ""
        print "[*] Entering '%s'" % rel_root    
        
        if any(original_extension in f for f in files):
            print "[*] Found %s file(s) in '%s'" % (original_extension, rel_root)
            new_folder = create_dir(new_dir)

        for file in files:
            if new_folder:
                if original_extension in file:
                    # f     = os.path.join(rel_root, file)
                    new_f = new_file_name(file)

                    print "[*] Converting : '%s' into '%s/%s'" % (file, relative_dir_name(new_dir), new_f)
                    
                    if convert(root, new_dir, file, new_extension, bitrate):
                        file_converted += 1
                    else:
                        has_error = True
                        error_files.append([root, file])
            else:
                "[-] Skipping %s" % rel_root

        print "[*] Leaving '%s'" % rel_root

    print ""
    print "[*] %d file(s) converted." % file_converted

    # Write the audio files that were skipped in a file for logging
    if has_error:
        try:
            with open("fichiers_erreurs.txt", "w") as f:
                p = pickle.Pickler(f)
                p.dump(error_files)
            f.close()
            print "[*] Error file created :  'fichiers_erreurs.txt'"
        except Exception, e:
            print "[-] Unable to create or open the file 'fichiers_erreurs.txt"
            print "[-] Error : %s " % e

else:
    print "[*] Exiting."
    sys.exit(0)

