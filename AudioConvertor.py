#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""AudioConverter 

Programm that permits to convert a music folder into another codec (i.e flac to mp3)
 
Usage:
    AudioConverter.py <original_codec> [options]
    AudioConverter.py -h | --help
    AudioConverter.py -v | --version
 
Options:
  -h, --help      
  -v, --version      
  --check               Check the number of file to convert before conversion       [default: False]
  --to=<codec>          Output codec                                                [default: mp3]
  --path=<path>         Path to the music folder (default is the current folder)
  --bitrate=<b>         Bitrate (64k, 128k, 192k...)                                [default: 128k]
  --output_file=<file>  Output file name                                            [default: AudioConverter_log_err.txt]

"""

import sys
import os
import settings
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
    docopt_arg = __doc__

    settings.init()

    arguments = docopt(docopt_arg, version='0.1')

    if arguments["<original_codec>"] is not None:
        settings.original_extension = arguments["<original_codec>"]
        settings.new_extension      = arguments["--to"]
        settings.bitrate            = arguments["--bitrate"]
        settings.logerror_file      = arguments["--output_file"] 
        settings.check_files        = arguments["--check"]

        if (arguments["--path"] is not None):
            path_to_folder = arguments["--path"]
        
print "Path to music folder : %s" % settings.path_to_folder
os.chdir(settings.path_to_folder)
settings.path_to_folder = os.getcwd()

if settings.check_files:
    if search_files():
        print "Continuing"

    else:
        print "[*] Exiting."
        sys.exit(0)


for root, dirs, files in os.walk(settings.path_to_folder):
    
    # Ignoring hidden folders/files recursively
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']

    # rel_root = relative_dir_name(root)

    print ""
    print "[*] Entering '%s'" % root    

    # Checking if there is any file matching our extension
    if any(settings.original_extension in f for f in files):
        print "[*] Found %s file(s) in '%s'" % (settings.original_extension, root)
        settings.dir_to_create = root + " - " + settings.new_extension
        
        # Checking if a directory for storing our converted files exist already
        # if it doesn't exist, we create it 
        if not os.path.isdir(settings.dir_to_create):
            if not create_dir():
                print "[-] Failed to create folder %s " % settings.dir_to_create
                sys.exit(0)

        # If it already exist
        else:
            print "[*] Folder %s exist." % settings.dir_to_create

            # We compare the two folders 
            # If there is the same amount of audio files in both
            if (compare_folder(root, settings.dir_to_create)):
                # We check the integrity of the files in our folder containing the converted audio files
                print "\t[*] Checking integrity of files"

                # If the integrity is correct, we change folder
                continue

            # if the content of the two folders is not the same we resume the conversion on the file that are missing 
            else:
                print "[*] Resuming conversion in %s " % root
            
        for file in files:
            if settings.original_extension in file:
                # f     = os.path.join(rel_root, file)
                new_f = new_file_name(file)
                
                print "[*] Converting : '%s' into '%s/%s'" % (file, settings.dir_to_create, new_f)
                
                if convert(root, file):
                    settings.file_converted += 1

    print "[*] Leaving '%s'" % root

print ""
print "[*] %d file(s) converted." % settings.file_converted
