#!/usr/bin/env python
'''
This script performs database dumps of all postgres databases in seperate
tarballs.

Prereqesites: linux :)
              python 2.7 or 3.4
              psql
              pg_dump

Usage: postgres.py [-h] [--dir DIR]

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   target directory to store the backups
              [default=/var/backups/postgres]

(c) Jochen S. Klar, November 2016
'''

import argparse
import os
import subprocess

fetch_databases_cmd = 'psql -l -t | cut -d"|" -f1 | sed -e "s/ //g" -e "/^$/d"'
dump_database_cmd = 'pg_dump %(database)s | gzip > "%(dir)s/%(database)s.gz"'

parser = argparse.ArgumentParser(description='This script performs database dumps of all postgres databases in seperate tarballs.')
parser.add_argument('--dir', action='store', default='/var/backups/postgres', help='target directory to store the backups [default=/var/backups/postgres]')

args = parser.parse_args()

# check if the target directory is there
if not os.path.isdir(args.dir):
    raise Exception('Could not find target directory %(dir)s.' % {'dir': args.dir})

# gather list of databases
databases = subprocess.check_output(fetch_databases_cmd, shell=True)

for database in databases.split()[1:]:
    if database not in ['template0', 'template1']:
        cmd = subprocess.call(dump_database_cmd % {
            'dir': args.dir,
            'database': database
        }, shell=True)
