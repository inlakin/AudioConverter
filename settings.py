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

# AudioConverter.py [--from=<codec>] [--to=<codec>] [--path=<path>] [--bitrate=<bitrate>] [--output_file=<file>]
from os import getcwd

# Extensions (i.e 'mp3', 'flac', 'ogg' ...)

original_extension = ""               # Must not be null
new_extension      = ""               # Optional, default : mp3
bitrate            = ""               # Optional, default : 128k
path_to_folder     = getcwd()         # Optional, default is the current folder
check_files        = False

new_dir            = ""
new_folder         = None


nb_files           = 0
file_converted     = 0
has_error          = False
error_files        = []

docopt_arg         = __doc__
