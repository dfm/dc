#!/usr/bin/env python
"""
Wrapper around git commit to keep track of stuff.

"""

import sys
import subprocess

cmd = "git commit "+" ".join(sys.argv[1:])

proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
ret  = proc.wait()
if ret == 0:
    print "Success..."
    print proc.communicate()[0]
else:
    print proc.communicate()[0]

