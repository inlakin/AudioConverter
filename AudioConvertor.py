#! /usr/bin/env python
# coding=utf-8

# TODO
# 
#  [*]  Recuperer les métadonnées des pistes
#  [*]  Progress Bar pendant le calcul du nombre de fichiers
#  [*]  Afficher avant de commencer un prompt pour prévenir l'utilisateur du nombre de fichiers trouvés à convertir et s'il veut continuer 
#  [ ]  Gérer les erreurs (try/catch)
#  [ ]  Ignorer les dossiers cachés lors de la recherche. 
#  
#  [ ]  Pouvoir proposer un format d'entrée et de sortie et bitrate en ligne de commande
#  [ ]  Permettre la reprise du travail si interruption
#  [ ]  (GUI)
#  

import os
import re
import sys
import pickle

from progress.spinner import Spinner
from pydub import AudioSegment
from pydub.utils import mediainfo

DIR_SUFFIXE          = " - MP3"
RELATIVE_DIR_PATTERN = r"\/([^\/\\]+)$"
FILE_SUFFIXE         = ".mp3"
FILE_PATTERN         = r"([^\/\\]+)\.flac$"

file_converted       = 0
nb_files             = 0

has_error            = False
error_files          = []



# For printing purposes : instead of printing the absolute path we are in, we print the relative one. 
def relative_dir_name(dirname):
    res = re.search(RELATIVE_DIR_PATTERN, str(dirname))
    if res:
        relative_path = res.group(1)
        return relative_path
    else:
        print "[-] relative_dir_name(dirname) function :  No match - Exiting .."
        sys.exit(0)


# Function that return a new name for the file we are converting (adding the correct extension)
def new_file_name(filename):
    new = re.search(FILE_PATTERN, str(filename))
    if new:
        new_file = new.group(1)
        return new_file
    else:
        print "[-] new_file_name(filename) function :  No match - Exiting .."
        sys.exit(0)


# Convert filename from the old_dir destination to the new_dir destination 
# MUST BE IMPROVED WITH the new_extension argument which will induce the writing of other functions (or not.. see pydub)
def convert(old_dir, new_dir,filename):

    print "\t[*] Processing ..."     
    sound = AudioSegment.from_file(old_dir+ "/" + filename)
    sound.export(new_dir + "/" + new_file_name(filename), format="mp3", bitrate="192k", tags=mediainfo(old_dir+ "/" + filename).get('TAG',{}))
    print "\t[*] Done."


# # # # # # # # # # # # #
#                       #
#       Main loop       #
#                       #
# # # # # # # # # # # # #

# Load the Spinner for checking the number of files to convert
spinner = Spinner('[*] Checking number of files to convert, please wait  ')

# Walk on every directories recursively to find how many audio files need to be converted
for dirname, dirnames, filenames in os.walk(os.getcwd()):
    spinner.next()
    for filename in filenames:
        if ".flac" in filename:
            nb_files += 1
print ""
print "[*] Finished. %s file(s) found" % nb_files

proceed = raw_input("[+] Do you want to continue ? (O/n) : ")
if proceed == 'O' or proceed == 'o':
    print "[*] Continuing."
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
                try:
                    convert(dirname, new_dir, filename)
                    file_converted += 1
                except UnicodeEncodeError as err_unicode_msg:
                    has_error = True
                    print "\t[-] Error" 
                    # print "\t[*] Exception : %s" % err_unicode_msg
                    # print "\t[*] Appending the file to the error list"
                    error_files.append([dirname, filename])

        print "[*] Leaving '%s'" % rel_dirname

    print ""
    print "[*] %d file(s) converted." % file_converted

    # Write the audio files that were skipped in a file for logging
    if has_error:
        try:
            with open("fichiers_erreurs.txt", "w") as f:
                p = pickle.Pickler(f)
                p.dump(error_files)
            f.close()
            print "[*] Error file created :  'fichiers_erreurs.txt'"
        except IOError as err_ioerror_msg:
            print "[-] Unable to open a file"
            print "[*] Exception : %s " % err_ioerror_msg

else:
    print "[*] Exiting."
    sys.exit(0)

