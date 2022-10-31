#!/usr/bin/env python3
'''
This script performs database dumps of all postgres databases in seperate
tarballs.

Prereqesites: linux :)
              python 3.4
              psql
              pg_dump

Usage: postgres.py [-h] [--dir DIR]

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   target directory to store the backups
              [default=/var/backups/postgres]
  --debug     verbose mode
  --dry       dry run

(c) Jochen S. Klar, 2016-2022
'''

import argparse
import os
import subprocess
from datetime import datetime, timezone

now = datetime.now(timezone.utc)

fetch_databases_cmd = 'psql -l -t | cut -d"|" -f1 | sed -e "s/ //g" -e "/^$/d"'
dump_database_cmd = 'pg_dump %(database)s | gzip > "%(dir)s/%(database)s%(date)s.sql.gz"'

parser = argparse.ArgumentParser(description='This script performs database dumps of all '
                                             'postgres databases in seperate tarballs.')
parser.add_argument('--dir', action='store', default='/var/backups/postgres',
                    help='target directory to store the backups [default=/var/backups/postgres]')
group = parser.add_mutually_exclusive_group()
group.add_argument('--date', action='store_true',
                   help='add the date to the filename')
group.add_argument('--datetime', action='store_true',
                   help='add the time and date to the filename')
parser.add_argument('--debug', action='store_true', help='verbose mode')
parser.add_argument('--dry', action='store_true', help='dry run')

args = parser.parse_args()

# check if the target directory is there
if not os.path.isdir(args.dir):
    raise Exception('Could not find target directory %(dir)s.' % {'dir': args.dir})

# create the date string for the filename
if args.date:
    date = '_' + now.date().isoformat()
elif args.datetime:
    date = '_' + now.isoformat()
else:
    date = ''

# gather list of databases
databases = subprocess.check_output(fetch_databases_cmd, shell=True).decode()

# loop over databases and create dumps
for database in databases.split():
    if database not in ['template0', 'template1']:
        cmd = dump_database_cmd % {
            'dir': args.dir,
            'database': database,
            'date': date
        }
        if args.debug:
            print(cmd)
        if not args.dry:
            subprocess.call(cmd, shell=True)
