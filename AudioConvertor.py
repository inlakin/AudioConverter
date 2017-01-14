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
from progress.bar import Bar 

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

nb_files_convert = 0

if settings.check_files:
    if search_files():
        print "[*] Continuing"

    else:
        print "[*] Exiting."
        sys.exit(0)


for root, dirs, files in os.walk(settings.path_to_folder):
    
    # Ignoring hidden folders/files recursively
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']

    # rel_root = relative_dir_name(root)

    print ""
    print "[*] Entering '%s'" % relative_dir_name(root)

    # Checking if there is any file matching our extension
    if any(settings.original_extension in f for f in files):
        print "[*] Found %s file(s) in '%s/%s'" % (settings.original_extension, os.pardir, relative_dir_name(root))
        settings.dir_to_create = root + " - " + settings.new_extension
        
        # Checking if a directory for storing our converted files exist already
        # if it doesn't exist, we create it 
        if not os.path.isdir(settings.dir_to_create):
            if not create_dir():
                print "[-] Failed to create folder '%s/%s' " % (os.pardir, relative_dir_name(settings.dir_to_create))
                sys.exit(0)

        # If it already exist
        else:
            print "[*] Folder '%s/%s' exist." % (os.pardir, relative_dir_name(settings.dir_to_create))

            # We compare the two folders 
            compare_folder(root, settings.dir_to_create)
                # We check the integrity of the files in our folder containing the converted audio files
            
            # if settings.files_to_convert is not None:
            if len(settings.files_to_convert) != 0 :
                
                print_files_to_convert()
                
                nb_files_convert = len(settings.files_to_convert)
                
                bar = Bar("Converting files in queue", max=nb_files_convert)
                
                for f in settings.files_to_convert:
                    # traceback_original_names(f)
                    bar.next()
                    old_dir = ""
                    old_file = ""
                    old_dir, old_file = os.path.split(f)
                    if convert(old_dir, old_file):
                        settings.file_converted += 1


            else:
                print "[*[ Head is up to date"
            # if the content of the two folders is not the same we resume the conversion on the file that are missing 
            print "[*] Resuming conversion in %s " % root
        
        nb_files_convert = nb_files_to_convert(root)

        bar = Bar("Converting %s" % relative_dir_name(root), max=nb_files_convert)

        # print "[*] NB FILES TO CONVERT : %d" % nb_files_to_convert

        for file in files:
            if settings.original_extension in file:
                # f     = os.path.join(rel_root, file)
                new_f = new_file_name(file)
                bar.next()
                
                print "[*] Converting : '%s' into '%s/%s'\r" % (file, relative_dir_name(settings.dir_to_create), new_f)
                

                if convert(root, file):
                    settings.file_converted += 1

        bar.finish()

    print "[*] Leaving '%s'" % relative_dir_name(root)

print ""
print "[*] %d file(s) converted." % settings.file_converted
