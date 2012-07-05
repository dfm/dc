#!/usr/bin/env python

import os

if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    data = open(os.path.join(dirname, "template.plist")).read()
    data = data.replace("{{ dirname }}", dirname)
    open(os.path.join(dirname, "ca.danfm.keys.plist"), "w").write(data)
