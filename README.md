A set of scripts to perform database dumps of all databases in seperate tarballs.

mysql.py
--------

```
usage: mysql.py [-h] [--dir DIR] [--debug] [--dry]

This script performs database dumps of all mysql and postgres database in
seperate tarballs.

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   target directory to store the backups
              [default=/var/backups/mysql]
  --debug     verbose mode
  --dry       dry run
```

postgres.py
-----------

```
usage: postgres.py [-h] [--dir DIR] [--debug] [--dry]

This script performs database dumps of all postgres databases in seperate
tarballs.

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   target directory to store the backups
              [default=/var/backups/postgres]
  --debug     verbose mode
  --dry       dry run
```

crontab configuration
---------------------

For a dump everyday at 1:00 use:

```
0 1 * * * /opt/dump/mysql.py
0 1 * * * su - postgres -c /opt/dump/postgres.py
```

(with mysql credentials in ~/.my.cnf)

(c) Jochen S. Klar, 2016
