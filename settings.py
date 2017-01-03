#! /usr/bin/env python
#
# -*- coding: utf-8 -*-

from os import getcwd
from docopt import docopt


# Extensions (i.e 'mp3', 'flac', 'ogg' ...)
original_extension   = ""
new_extension        = ""
bitrate              = ""
path = getcwd()
pattern_relative_dir = r"\/([^\/\\]+)$"
pattern_file         = r"([^\/\\]+)\." + original_extension + "$"

nb_files             = 0
file_converted       = 0
has_error            = False
error_files          = []

doc = '''
Usage:
---------
    ./AudioConverter.py -r [--from=<codec>] [--to=<codec>] [--path=<path>] [--bitrate=<n>]
    ./AudioConverter.py --run
    ./AudioConverter.py (-h | --help)
Options:
---------
    -r, --run               Run the program 
    -f, --from=<codec>      original codec
    -t, --to=<codec>        destination codec
    -p, --path=<path>       path towards the music folder
    -b, --bitrate=<n>       bitrate (32k, 64k, 128k, 192k, 320k)
    -h, --help              Show this screen and exit.
Examples:
---------
    ./AudioConvertor.py -t='flac' -t='mp3' -p='/home/user/music/'
    ./AudioConvertor.py -t='mp3 -b='192k'"
Default:
---------
    By default, the program runs with the following argument : 
        Output codec = MP3
        Bitrate      = 128k
        Path         = current_path

'''