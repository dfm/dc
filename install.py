#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
from subprocess import call, check_call

if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    data = open(os.path.join(dirname, "template.plist")).read()
    data = data.replace("{{ dirname }}", dirname)

    # Save the script.
    k = "io.dfm.keys.plist"
    fn = os.path.join(os.path.expanduser("~/Library/LaunchAgents"), k)
    print("Saving file {0}".format(fn))
    open(fn, "w").write(data)

    # Launch the process.
    cmd = "launchctl unload " + fn
    print("Running: {0}".format(cmd))
    call(cmd.split())

    cmd = "launchctl load " + fn
    print("Running: {0}".format(cmd))
    check_call(cmd.split())
