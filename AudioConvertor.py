#! /usr/bin/env python
# coding=utf-8

# TODO
# 
#  [*]  Recuperer les métadonnées des pistes
#  [*]  Progress Bar pendant le calcul du nombre de fichiers
#  [*]  Afficher avant de commencer un prompt pour prévenir l'utilisateur du nombre de fichiers trouvés à convertir et s'il veut continuer 

#  [ ]  Ignorer les dossiers cachés lors de la recherche. 
#  [ ]  Gérer les erreurs (try/catch)
# 
#  [ ]  Format dans le fichier d'erreur 
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
def relative_dir_name(root):
    res = re.search(RELATIVE_DIR_PATTERN, str(root))
    if res:
        relative_path = res.group(1)
        return relative_path
    else:
        print "[-] relative_dir_name(root) function :  No match - Exiting .."
        sys.exit(0)


# Function that return a new name for the file we are converting (adding the correct extension)
def new_file_name(file):
    new = re.search(FILE_PATTERN, str(file))
    if new:
        new_file = new.group(1)
        return new_file
    else:
        print "[-] new_file_name(file) function :  No match - Exiting .."
        sys.exit(0)


# Convert file from the old_dir destination to the new_dir destination 
# MUST BE IMPROVED WITH the new_extension argument which will induce the writing of other functions (or not.. see pydub)
def convert(old_dir, new_dir,file):

    print "\t[*] Processing ..."     
    sound = AudioSegment.from_file(old_dir+ "/" + file)
    sound.export(new_dir + "/" + new_file_name(file), format="mp3", bitrate="192k", tags=mediainfo(old_dir+ "/" + file).get('TAG',{}))
    print "\t[*] Done."


# # # # # # # # # # # # #
#                       #
#       Main loop       #
#                       #
# # # # # # # # # # # # #

# Load the Spinner for checking the number of files to convert
spinner = Spinner('[*] Checking number of files to convert, please wait  ')

# Walk on every directories recursively to find how many audio files need to be converted
for root, dirs, files in os.walk(os.getcwd()):
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']
    spinner.next()
    for file in files:
        if ".flac" in file:
            nb_files += 1
print ""
print "[*] Finished. %s file(s) found" % nb_files

proceed = raw_input("[+] Do you want to continue ? (O/n) : ")
if proceed == 'O' or proceed == 'o':
    print "[*] Continuing."
    for root, dirs, files in os.walk(os.getcwd()):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        rel_root = relative_dir_name(root)
        
        print ""
        print "[*] Entering '%s'" % rel_root    
        # for subroot in dirs:
        #     print("[*] Found directory : " + os.path.join(rel_root, subroot))

        if any("flac" in f for f in files):
            new_dir = root + DIR_SUFFIXE
            print "[*] Found flac file(s) in '%s'" % rel_root
            print "[*] Creating new directory : '%s'" % new_dir
            os.mkdir(new_dir)

        for file in files:
            if ".flac" in file:

                # f     = os.path.join(rel_root, file)
                new_f = new_file_name(file) + FILE_SUFFIXE

                print "[*] Converting : '%s' into '%s/%s'" % (file, relative_dir_name(new_dir), new_f)
                try:
                    convert(root, new_dir, file)
                    file_converted += 1
                except Exception, e:
                    has_error = True
                    print "\t[-] Unable to convert."
                    print "\t[-] Error : %s " % e 
                    # print "\t[*] Exception : %s" % err_unicode_msg
                    # print "\t[*] Appending the file to the error list"
                    error_files.append([root, file])

        print "[*] Leaving '%s'" % rel_root

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
        except Exception, e:
            print "[-] Unable to create or open the file 'fichiers_erreurs.txt"
            print "[-] Error : %s " % e

else:
    print "[*] Exiting."
    sys.exit(0)

