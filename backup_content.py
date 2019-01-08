#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from sys import argv

import os
import tarfile

CONTENT_DIR="/var/www/html"
DESTINATION_DIR="/opt/backup"
DAYS = 30
DATABASE = "eircstarterkit3"

def help():
    print "Usage: " + "python " + argv[0] + " " + "ARGS"
    print ("\nPossible args:\n")
    print ("--all: (SELECTED BY DEFAULT): Performs a backup of files, a dump of the database and deletes old backups")
    print ("--content: Performs a backup of files")
    print ("--mysql: Performs a dump of the database")
    print ("--delete: Deletes old backups")
    print ("--help: Displays this help prompt")
    print ("--verbose: Display extra text")
    print 


def get_string_date(debug=False):
    today = datetime.now().replace(microsecond=0)
    str_format = today.isoformat('_')
    # To avoid problems with tar
    str_format = str_format.replace(":", '-')
    if debug:
        print "Today is {}".format(str_format)
    return str_format

"""
def backup_content(debug=False):
    global CONTENT_DIR
    global DESTINATION_DIR

    if not os.path.isdir(CONTENT_DIR):
        print "NO FOLDER TO BACK UP"
        exit(1)

    if not os.path.isdir(DESTINATION_DIR):
        if debug:
            print "Destination folder not present. Creating {}".format(DESTINATION_DIR)
        os.mkdir(DESTINATION_DIR)

    filename = CONTENT_DIR.split(os.sep)[-1]
    destination_filename = DESTINATION_DIR + os.sep + "backup" + "_" + filename + "_" + get_string_date() + ".tar.gz"

    if debug:
        print "Backup filename will be {}".format(destination_filename)
    try:
        with tarfile.open(destination_filename, "w:gz") as backup:
            if debug:
                print "Folder {} will be tared as {}".format(CONTENT_DIR, filename)
            backup.add(CONTENT_DIR, filename)
    except:
        print "ERROR performing backup. Exiting..."
        exit(1)
"""

def get_days_since(backup_date_str):
    backup_date = datetime.strptime(backup_date_str, "%Y-%m-%d")
    delta = datetime.now() - backup_date 
    return delta.days

def delete_old_backups(debug=False,delete=True):
    global DESTINATION_DIR
    global DAYS
    
    for backup in os.listdir(DESTINATION_DIR):
        try:
            backup.index(".gz")
        except:
            if debug:
                print "Not a backup. Skipping"
            continue
        
        # CONTENT_DIR.split(os.sep)[-1]
        backup_type = backup.split("_")[1]

        if debug:
            print "Handling \"{}\"...".format(backup)
            print "backup_type is {}".format(backup_type)
        
        time_str = backup.split(backup_type + "_")[1]
        time_str = time_str.split(".")[0]
        backup_date_str = time_str.split("_")[0]

        days = get_days_since(backup_date_str)
        if debug:
                print "Backup \"{}\" is {} day(s) old".format(backup, days)
        if  days >= DAYS:
            file_2_delete = DESTINATION_DIR + os.sep + backup
            if debug:
                print "Deleting {}".format(file_2_delete)
            if delete:
                os.remove(file_2_delete)

"""
def dump_mysql(debug=False):
    global DATABASE
    global DESTINATION_DIR
    filename = "backup_mysql_" + get_string_date(False)
    backup_path = DESTINATION_DIR + os.sep + filename + ".sql.gz"
    command = "mysqldump --single-transaction {} | gzip -c > {}".format(DATABASE, backup_path)

    if debug:
        print("dump command is {}".format(command))
    
    try:
        os.system(command)
    except:
        print "ERROR performing dump. Exiting..."
        exit(1)
"""

def date_ansible_backups(debug=False):
    """
        Ahora, espera nombres del estilo
        TIPO{{ inventory_hostname }}.tar.gz"
        donde tipo es WEB o DATABASE
    """
    """ pseudo codigo """
    TYPES = ["DATABASE", "WEB"]
    REPLACEMENTS = ["DATABASE":"mysql", "WEB":"html"]
    for backup in os.listdir(DESTINATION_DIR):
        for type in TYPES:
            try:
                backup.index(type)
                new_name = backup.replace(type, "backup_{}_{}".format(
                    REPLACEMENTS[type],
                    get_string_date()
                ))
                os.rename(backup, new_name)
            except:
                if debug:
                    print "Not an Ansible backup. Skipping"
                continue

"""
    TODO: Revisar el flujo de ejecución nuevo
"""
def main():
    if len(argv) == 1:
        print "No args provided. Launching all..."
        # backup_content()
        # dump_mysql()
        date_ansible_backups()
        # delete_old_backups()
    else:
        if "--help" in argv:
            help()
            exit(0)
        
        if "--verbose" in argv:
            verbose = True
        else:
            verbose = False

        if "--all" in argv:
            backup_content(verbose)
            dump_mysql(verbose)
            delete_old_backups(verbose)
        else:
            if "--content" in argv:
                backup_content(verbose)
            if "--mysql" in argv:
                dump_mysql(verbose)
            if "--delete" in argv:
                delete_old_backups(verbose)

if __name__ == "__main__":
    main()

