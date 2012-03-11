#!/usr/bin/env python
"""
Wrapper around git commit to keep track of stuff.

"""

import os
import sys
import subprocess
import re
import datetime
import sqlite3

args = " ".join([a if " " not in a else "\""+a+"\"" for a in sys.argv[1:]])
if re.search("\-[a-zA-Z]*m", args) is None:
    print "You need to use the command line message for now... sorry!"
    sys.exit(1)
cmd = "git commit "+args
print "Running:", cmd

# Run the commit command
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
ret  = proc.wait()
if ret != 0:
    print proc.communicate()[0]
    sys.exit(ret)

# Parse return values
o = proc.communicate()[0]
g = re.search("(.*?) files changed, (.*?) insertions\(\+\),"\
    +"(.*?) deletions\(\-\)", o).groups()
print o

# Get the remote info
dirs = list(os.path.split(os.path.abspath(__file__)))
i = 1
for i in range(1, len(dirs)):
    if os.path.exists(os.path.join(*(dirs[:-i] + [".git"]))):
        break
bd = os.path.join(*(dirs[:-i]))

# Update the database
db_fn = os.path.join(*(dirs[:-1]+[".gc.db"]))
db = sqlite3.connect(db_fn)
cursor = db.cursor()
cursor.execute("""create table if not exists commits
    (id integer primary key, files integer, insertions integer,
    deletions integer, dir text, date text)""")
date = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
cursor.execute("insert into commits values (null,?,?,?,?,?)",
            list(g)+[bd,date])
db.commit()
cursor.close()


