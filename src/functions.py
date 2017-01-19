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
        logerr = open(settings.logerr_file, "a")
        logerr.write("\nERR : REL_DIR_NAME, No match for %s" % root)
        logerr.close()
        print "[-] relative_dir_name(root) function :  No match - Exiting .."


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
        logerr = open(settings.logerr_file, "a")
        logerr.write("\nERR : NEW_FILE_NAME(), No match for %s" % file)
        logerr.close()
        print "[-] new_file_name(file) function :  No match"


def nb_files_to_convert(folder):
    """ Return the number of files to convert in a specific folder
    
    Args:
        The folder to check in 

    Return:
        (int) : the number of files to convert
    """
    original_files = 0

    ls_original_folder = os.listdir(folder)

    for elt in ls_original_folder:
        if settings.original_extension in elt:
            original_files += 1

    # for root, dirs, files in os.walk(folder):
    #     for file in files:
    #         if settings.original_extension in file:
    #             original_files +=1

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
    
    ls_original_folder        = []
    ls_new_folder             = []
    original_files            = []
    new_files                 = []
    
    settings.files_to_check   = []
    settings.files_to_convert = []
    

    print "[*] Comparing %s to %s" % (relative_dir_name(folder), relative_dir_name(new_folder))

    ls_original_folder = os.listdir(folder)
    ls_new_folder      = os.listdir(new_folder)

    #   Populating the list of files to convert
    for elt in ls_original_folder:
        if settings.original_extension in elt:
            original_files.append(folder + "/" + elt)

    #   Populating the files already converted
    for elt in ls_new_folder:
        if settings.new_extension in elt:
            new_files.append(folder + "/" + elt)

    print "\t[*] %d files to convert" % len(original_files)
    print "\t[*] %d files in destination folder" % len(new_files)

    #   Generating a list of files to convert if not converted and a list of files that need an integrity check
    for old_f in original_files:
        base_old_f = os.path.splitext(os.path.basename(old_f))

        if any(base_old_f[0] in new_f for new_f in new_files):
            settings.files_to_check.append(new_folder + "/" + base_old_f[0] + "." + settings.new_extension)
        else:
            settings.files_to_convert.append(old_f)


    if len(settings.files_to_convert) != 0:
        print ""
        print "\t[*] Need to convert :"
        for f in settings.files_to_convert:
            print "\t\t- %s" % relative_dir_name(f)

    if len(settings.files_to_check) != 0:
        print ""
        print "\t[*] Need to check integrity for : "
        for f in settings.files_to_check:
            print "\t\t- %s " % relative_dir_name(f)

        print "[*] Launching integrity check .."
        print ""
        for f in settings.files_to_check:
            # s = AudioSegment.from_mp3(file_check)
            check = mediainfo(f)
            if check:
                print "[*] Integrity" + colored(" PASSED ", 'green')  + "for %s" % relative_dir_name(f)
            else:
                print "[" + colored("-","red") + "] Integrity" + colored(" FAILED ", 'red')  + "for %s" % f
                logerr = open(settings.logerr_file, 'a')
                st = time.time()
                ts = datetime.datetime.fromtimestamp(st).strftime('%Y-%m-%d %H:%M:%S')
                logerr = open(settings.logerr_file, "a")
                logerr.write("[" + str(ts) + "]\n")
                logerr.write("Integrity FAILED for %s" % f)
                logerr.close()
                traceback_original_names(f)
                # print "Appending %s/%s to files_to_convert" % (settings.queue_dir, settings.queue_file)    
                settings.files_to_convert.append(settings.queue_dir + "/" + settings.queue_file)
        
        print ""

        removeTmpFile("/tmp/")
   
   
def removeTmpFile(folder):
    
    pattern = r"tmp[\w\W]+"
    ls_folder = os.listdir(folder)

    for elt in ls_folder:
        res = re.search(pattern, elt)
        if res:
            try:
                os.remove(folder + "/" + elt)
                st = time.time()
                ts = datetime.datetime.fromtimestamp(st).strftime('%Y-%m-%d %H:%M:%S')
                logerr = open(settings.logerr_file, "a")
                logerr.write("[" + str(ts) + "]\n")
                logerr.write("[*] Deleting tmp audio file %s/%s" % (folder,elt))
                logerr.close()
            except Exception, e:
                print e

    print "%s is clean" % folder


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
        
        settings.files_not_converted.append(old_dir + "/" + file)
        settings.nb_files_not_converted += 1 
        
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


