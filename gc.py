#!/usr/bin/env python
"""
Wrapper around git commit to keep track of stuff.

"""

import sys
import subprocess
import re

args = " ".join([a if " " not in a else "\""+a+"\"" for a in sys.argv[1:]])
if re.search("\-[a-zA-Z]*m", args) is None:
    print "You need to use the command line message for now... sorry!"
    sys.exit(1)
cmd = "git commit "+args
print "Running:", cmd

proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
ret  = proc.wait()
if ret != 0:
    print proc.communicate()[0]
    sys.exit(ret)

o = proc.communicate()[0]
g = re.search("(.*?) files changed, (.*?) insertions\(\+\),"\
    +"(.*?) deletions\(\-\)", o).groups()
print g

print o

