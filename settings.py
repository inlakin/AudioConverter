#! /usr/bin/env python
#
# -*- coding: utf-8 -*-


# Extensions (i.e 'mp3', 'flac', 'ogg' ...)
original_extension   = ""
new_extension        = ""
bitrate              = ""

pattern_relative_dir = r"\/([^\/\\]+)$"
pattern_file         = r"([^\/\\]+)\." + original_extension + "$"

nb_files             = 0
file_converted       = 0
has_error            = False
error_files          = []