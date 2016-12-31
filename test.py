#! /usr/bin/env python

import os
import re
import sys

from pydub import AudioSegment

DIR_SUFFIXE          = " - MP3"
RELATIVE_DIR_PATTERN = r"\/([.]+)$"
FILE_SUFFIXE         = ".mp3"
FILE_PATTERN         = r"([\w\ \(\)\-]+)\.flac$"

file_converted = 0

def relative_dir_name(dirname):
    res = re.search(RELATIVE_DIR_PATTERN, str(dirname))
    if res:
        relative_path = res.group(1)
        return relative_path
    else:
        print "[-] relative_dir_name(dirname) function :  No match - Exiting .."
        sys.exit(0)


def new_file_name(filename):
    new = re.search(FILE_PATTERN, str(filename))
    if new:
        new_file = new.group(1)
        return new_file
    else:
        print "[-] new_file_name(filename) function :  No match - Exiting .."
        sys.exit(0)


def convert(old_dir, new_dir,filename):

    print "\t[*] Processing ..."     
    sound = AudioSegment.from_file(old_dir+ "/" + filename)
    sound.export(new_dir + "/" + new_file_name(filename), format="mp3", bitrate="192k")
    print "\t[*] Done."

 
for dirname, dirnames, filenames in os.walk(os.getcwd()):

    rel_dirname = relative_dir_name(dirname)
    
    print ""
    print "[*] Entering '%s'" % rel_dirname    
    # for subdirname in dirnames:
    #     print("[*] Found directory : " + os.path.join(rel_dirname, subdirname))

    if any("flac" in f for f in filenames):
        new_dir = dirname + DIR_SUFFIXE
        print "[*] Found flac file(s) in '%s'" % rel_dirname
        print "[*] Creating new directory : '%s'" % new_dir
        os.mkdir(new_dir)

    for filename in filenames:
        if ".flac" in filename:

            # f     = os.path.join(rel_dirname, filename)
            new_f = new_file_name(filename) + FILE_SUFFIXE

            print "[*] Converting : '%s' into '%s/%s'" % (filename, relative_dir_name(new_dir), new_f)
            convert(dirname, new_dir, filename)
            file_converted += 1

    print "[*] Leaving '%s'" % rel_dirname

print ""
print "[*] %d file(s) converted." % file_converted
