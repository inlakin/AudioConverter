#! /usr/bin/env python
#
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

from os import getcwd


def init():
    global original_extension
    global new_extension
    global bitrate
    global logerr_file
    global check_files
    global path_to_folder
    
    global dir_to_create
    global new_folder
    
    global nb_converted_file
    global nb_files
    global file_converted
    global docopt_arg

    original_extension = ""               # Must not be null
    new_extension      = ""               # Optional, default : mp3
    bitrate            = ""               # Optional, default : 128k
    logerr_file        = "logerr.txt"
    check_files        = False
    path_to_folder     = getcwd()         # Optional, default is the current folder
    dir_to_create      = ""
    new_folder         = None

    nb_converted_file  = 0
    nb_files           = 0
    file_converted     = 0

    docopt_arg         = __doc__
