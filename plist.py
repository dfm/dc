#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys

if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    data = open(os.path.join(dirname, "data/template.plist")).read()
    data = data.replace("{{ dirname }}", dirname)

    # Save the script.
    k = sys.argv[1] if len(sys.argv) > 1 else "io.dfm.keys.plist"
    fn = os.path.join(os.path.expanduser("~/Library/LaunchAgents"), k)
    print("Saving file {0}".format(fn))
    open(fn, "w").write(data)
