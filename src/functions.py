#! /usr/bin/env python
#
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import datetime

from termcolor import colored
from pydub import AudioSegment
from pydub.utils import mediainfo

import settings
from progress.spinner import Spinner


def search_files():
    """ Function that search the number of files to convert, output the result and then ask the user if he wants to proceed with the conversion of the files 

        Args:
            path (str): The path to search (recursively)

        Return:
            bool: True if the user wants to convert them, False otherwise
    """

    spinner = Spinner('[*] Checking number of files to convert, please wait  ')
    
    for root, dirs, files in os.walk(settings.path_to_folder):
        # Test for not searching into hidden folder(s)
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        spinner.next()
        for file in files:
            if settings.original_extension in file:
                settings.nb_files += 1
    print ""
    print "[*] In directory %s " % settings.path_to_folder
    print "[*] Finished. %s %s file(s) found" % (settings.nb_files, settings.original_extension)

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


def new_file_name(file):
    """ Function that returns the new name of the file we are converting

        Args:
            file (str): the original file name (i.e 'Apparat - Circle.flac')

        Returns
            str: the new file name (i.e 'Apparat - Circle.mp3')
    """
    pattern_file = r"([^\/\\]+)\." + settings.original_extension + "$"
    res = re.search(pattern_file, str(file))
    if res:
            new_file = res.group(1) + "." + settings.new_extension
            return new_file
    else:
        print "[-] new_file_name(file) function :  No match - Exiting .."
        sys.exit(0)


def nb_files_to_convert(folder):
    """ Return the number of files to convert in a specific folder
    
    Args:
        The folder to check in 

    Return:
        (int) : the number of files to convert
    """
    original_files = 0

    for root, dirs, files in os.walk(folder):
        for file in files:
            if settings.original_extension in file:
                original_files +=1

    return original_files


def print_files_to_convert():

    print ""
    print "[*] Files to convert in queue"
    for f in settings.files_to_convert:
        print "    -  %s" % f
    print ""

def compare_folder(folder, new_folder):
    """ Procedure that compare the audio content of two given folder based on the extension provided in parameters
        It is updating the global variables files_to_convert and files_to_check in order to access them in the main loop
        
        Args:
            folder (str) : Path to the old folder containing the previous extension
            new_folder (str) : Path to the new folder containing the right extension

    """
    original_files   = []
    new_files        = []
    # integrity      = True
    
    # file_pattern     = r"(^[\w\W]+)\.[\w]+$"

    print "[*] Comparing %s to %s" % (relative_dir_name(folder), relative_dir_name(new_folder))

    # Walking into the dir we want to convert to find the original files
    for root, dirs, files in os.walk(folder, topdown=False):
        for file in files:
            if settings.original_extension in file:
                original_files.append(root+ "/" +file)
    print "\t[*] %s files to convert in %s" % (len(original_files), relative_dir_name(folder))

    # Walking into the dir that exist to check which files are created
    for root, dirs, files in os.walk(new_folder):
        for file in files:
            if settings.new_extension in file:
                new_files.append(root + "/" + file)
    print "\t[*] %s files converted in %s" % (len(new_files), relative_dir_name(new_folder))



    for old_f in original_files:

        dirname, filename = os.path.split(old_f)
        basename_old_f = os.path.splitext(filename)

        if any(basename_old_f[0] in new_f for new_f in new_files):
            settings.files_to_check.append(basename_old_f[0] + "." + settings.new_extension)

        else:
            settings.files_to_convert.append(old_f)


    if len(settings.files_to_convert) != 0:
        print ""
        print "\t[*] Need to convert :"
        for f in settings.files_to_convert:
            print "\t\t- %s" % f

    if len(settings.files_to_check) != 0:
        print ""
        print "\t[*] Need to check integrity for : "
        for f in settings.files_to_check:
            print "\t\t- %s " % f

        proceed = raw_input("[*] Continue with files integrity check ? (O/n) : ")
        print ""
        if proceed == "O" or proceed == "o":
            for f in settings.files_to_check:
                file_check = new_folder + "/" + f
                # s = AudioSegment.from_mp3(file_check)
                check = mediainfo(file_check)
                if check:
                    print "[*] Integrity" + colored(" PASSED ", 'green')  + "for %s" % f
                else:
                    print "[" + colored("-","red") + "] Integrity" + colored(" FAILED ", 'red')  + "for %s" % f
                    traceback_original_names(file_check)
                    # print "Appending %s/%s to files_to_convert" % (settings.queue_dir, settings.queue_file)    
                    settings.files_to_convert.append(settings.queue_dir + "/" + settings.queue_file)
            
            print ""
            raw_input("Press any key to continue ... ")
        else:
            print "[*] Exiting program"
            sys.exit(0)
    
    # if len(original_files) == len(new_files):
    #     print "[*] Checking integrity"
    #     if integrity == True:
    #         print "[*] Moving to next folder"
    #     else:
    #         print "[*] Integrity check failed for "

    
    # if original_files == new_files:
    #     return True
    # else:
    #     return False


def create_dir():
    
    """ Create a new directory for storing the new converted elements

        Return:
            bool: True if the creation has succeed, False otherwise

    """


    print "[*] Creating new directory : '%s'" % settings.dir_to_create
    try:
        os.mkdir(settings.dir_to_create)
        return True
    except Exception, e:
        print "[-] Error : %s" % e 
        return False


def convert(old_dir,file):

    """ Function that calls the PyDub library to convert the file passed in argument

        Args:
            old_dir (str):  Previous directory the file is in (i.e '/music/Apparat/DJ-Kicks/')
            new_dir (str):  New directory the file will be in (i.e '/music/Apparat/DJ-Kicks - MP3/')
            file (str):     the file we want to convert

        Return:
            bool: True if the conversion has been successful, False otherwise
    """
    # print "Converting into %s " % settings.dir_to_create
    # print "\t[*] Processing ..."   
    try:
        sound = AudioSegment.from_file(old_dir+ "/" + file)
        sound.export(settings.dir_to_create + "/" + new_file_name(file), format=settings.new_extension, bitrate=settings.bitrate, tags=mediainfo(old_dir+ "/" + file).get('TAG',{}))
        # print "\t[*] Done."
        return True

    except Exception, e:
        st = time.time()
        ts = datetime.datetime.fromtimestamp(st).strftime('%Y-%m-%d %H:%M:%S')
        logerr = open(settings.logerr_file, 'a')
        logerr.write("[" + str(ts) + "]\n")
        logerr.write("\tFile : %s/%s\n" % (old_dir, file))
        logerr.write("\t%s\n" % e)
        logerr.close()
        print "\t[-] Error: %s " % e 
        return False


def traceback_original_names(basename):
    """ Updates globals queue_dir and queue_file

    Args:
        basename (str) : path to a 

    """
    tmp_queue_dir = ""
    tmp_queue_file = ""
    basename_tmp_queue_file = ""
    original_dir_pattern = r"([\w\W]+)\ \-\ mp3"

    # Handle global settings.queue_dir
    tmp_queue_dir, tmp_queue_file = os.path.split(basename)
    res = re.search(original_dir_pattern, tmp_queue_dir)
    

    if res:
        settings.queue_dir = res.group(1)
    else:
        print "ERR: traceback_original_names(): no match found for %s " % tmp_queue_dir
        sys.exit(0)

    # Handle global queue_file
    basename_tmp_queue_file = os.path.splitext(tmp_queue_file)
    settings.queue_file = basename_tmp_queue_file[0] + "." + settings.original_extension


    # print "Traceback returned\n\tPath: %s\n\tFile: %s" % (settings.queue_dir, settings.queue_file)


