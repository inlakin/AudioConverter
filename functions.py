#! /usr/bin/env python
#
# -*- coding: utf-8 -*-

import os
import re
import sys
from pydub import AudioSegment
from pydub.utils import mediainfo

from settings import *
from progress.spinner import Spinner


def search_files(path, original_extension, nb_files):
    """ Function that search the number of files to convert, output the result and then ask the user if he wants to proceed with the conversion of the files 

        Args:
            path (str): The path to search (recursively)

        Return:
            bool: True if the user wants to convert them, False otherwise
    """

    spinner = Spinner('[*] Checking number of files to convert, please wait  ')
    
    for root, dirs, files in os.walk(path):
        # Test for not searching into hidden folder(s)
        # files = [f for f in files if not f[0] == '.']
        # dirs[:] = [d for d in dirs if not d[0] == '.']
        spinner.next()
        for file in files:
            if original_extension in file:
                nb_files += 1
    print ""
    print "[*] In directory %s " % path
    print "[*] Finished. %s %s file(s) found" % (nb_files, original_extension)

    proceed = raw_input("[+] Do you want to continue ? (O/n) : ")
    if proceed == 'O' or proceed == 'o':
        return True
    else:
        return False


def relative_dir_name(root):
    """ Function that returns the relative path of the current directory
        
        Args:
            root (str): the current absolute path

        Returns:
            str: The relative path
    """
    pattern_relative_dir = r"\/([^\/\\]+)$"

    res = re.search(pattern_relative_dir, str(root))
    if res:
        relative_path = res.group(1)
        return relative_path
    else:
        print "[-] relative_dir_name(root) function :  No match - Exiting .."
        sys.exit(0)


def new_file_name(file, original_extension, new_extension):
    """ Function that returns the new name of the file we are converting

        Args:
            file (str): the original file name (i.e 'Apparat - Circle.flac')

        Returns
            str: the new file name (i.e 'Apparat - Circle.mp3')
    """
    print "new file name ; new_extension %s" % new_extension
    print "new_file_name(%s,%s,%s)" % (file, original_extension, new_extension)
    pattern_file = r"([^\/\\]+)\." + original_extension + "$"
    res = re.search(pattern_file, str(file))
    if res:
            new_file = res.group(1) + "." + new_extension
            return new_file
    else:
        print "[-] new_file_name(file) function :  No match - Exiting .."
        sys.exit(0)


def create_dir(root, new_extension):
    
    """ Create a new directory for storing the new converted elements

        Args:
            new_dir (str): Name of the directory without the extension

        Return:
            bool: True if the creation has succeed, False otherwise

    """
    new_dir = root + " - " + new_extension
    print "[*] Creating new directory : '%s'" % new_dir
    try:
        os.mkdir(new_dir)
        return new_dir
    except Exception, e:
        print "[-] Error : %s" % e 
        return False


def convert(old_dir, new_dir,file, original_extension, new_extension, bit):

    """ Function that calls the PyDub library to convert the file passed in argument

        Args:
            old_dir (str):  Previous directory the file is in (i.e '/music/Apparat/DJ-Kicks/')
            new_dir (str):  New directory the file will be in (i.e '/music/Apparat/DJ-Kicks - MP3/')
            file (str):     the file we want to convert
            new_extension (str) (optional, default=mp3): the output codec 
            bitrate (str) (optional, default=128k): the bitrate

        Return:
            bool: True if the conversion has been successful, False otherwise
    """

    print "\t[*] Processing ..."   
    print "\t Args : old_dir %s\n new_dir %s\n file %s\n new_extension %s\n bit %s" % (old_dir, new_dir, file, new_extension, bit)
    # try:
    sound = AudioSegment.from_file(old_dir+ "/" + file)
    sound.export(new_dir + "/" + new_file_name(file, original_extension, new_extension), format=new_extension, bitrate=bit, tags=mediainfo(old_dir+ "/" + file).get('TAG',{}))
    print "\t[*] Done."
    return True

    # except Exception, e:
    #     print "\t[-] Error: %s " % e 
        # return False
