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

# Database
dirs = list(os.path.split(os.path.abspath(__file__)))
db_fn = os.path.join(*(dirs[:-1]+[".gc.db"]))
db = sqlite3.connect(db_fn)
cursor = db.cursor()

if "--info" in sys.argv:
    try:
        N = int(sys.argv[sys.argv.index("--info")+1])
    except:
        N = 10
    for d in cursor.execute("""select * from commits order by id desc
            limit ?""", (N,)):
        print d
    cursor.close()
    sys.exit(0)

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
print o,
g = re.search("\[.*?\] (.*?) ([0-9]*?) files changed.*?([0-9]*?) insertions.*?"\
    +"([0-9]*?) deletions", o, flags=re.M|re.S).groups()

# Get the remote info
i = 1
for i in range(1, len(dirs)):
    if os.path.exists(os.path.join(*(dirs[:-i] + [".git"]))):
        break
bd = os.path.join(*(dirs[:-i]))

# Update the database
cursor.execute("""create table if not exists commits
    (id integer primary key, message text, files integer, insertions integer,
    deletions integer, dir text, year integer, month integer,
        day integer, weekday integer, time real)""")
d = datetime.datetime.now()
ts = (d.hour*60+d.minute)*60+d.second+d.microsecond*1e-6
date = [d.year, d.month, d.day, d.weekday(), ts]
cursor.execute("insert into commits values (null,?,?,?,?,?,?,?,?,?,?)",
            list(g)+[bd]+date)
db.commit()
cursor.close()

