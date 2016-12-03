#!/usr/bin/env python
'''
This script performs database dumps of all mysql and postgres database in
seperate tarballs.

Prereqesites: linux :)
              python 2.7 or 3.4
              mysql
              mysqldump

Usage: mysql.py [-h] [--dir DIR]

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   target directory to store the backups
              [default=/var/backups/mysql]

(c) Jochen S. Klar, November 2016
'''

import argparse
import os
import subprocess

fetch_databases_cmd = 'mysql -e "SHOW DATABASES;"'
dump_database_cmd = 'mysqldump --lock-tables --complete-insert --add-drop-table --quick --quote-names --databases %(database)s | gzip > "%(dir)s/%(database)s.gz"'

parser = argparse.ArgumentParser(description='This script performs database dumps of all mysql and postgres database in seperate tarballs.')
parser.add_argument('--dir', action='store', default='/var/backups/mysql', help='target directory to store the backups [default=/var/backups/mysql]')
parser.add_argument('--debug', action='store_true', help='verbose mode')
parser.add_argument('--dry', action='store_true', help='dry run')

args = parser.parse_args()

# check if the target directory is there
if not os.path.isdir(args.dir):
    raise Exception('Could not find target directory %(dir)s.' % {'dir': args.dir})

# gather list of databases
databases = subprocess.check_output(fetch_databases_cmd, shell=True)

for database in databases.split()[1:]:
    if database not in ['information_schema', 'performance_schema', 'sys']:
        cmd = dump_database_cmd % {
            'dir': args.dir,
            'database': database
        }
        if args.debug:
            print cmd
        if not args.dry:
          subprocess.call(cmd, shell=True)
