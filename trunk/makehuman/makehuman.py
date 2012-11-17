#!/usr/bin/env python


import sys
import os
import str

sys.path.append('core')

from debugdump import DebugDump

# print os.getcwd()

__version__ = filter(str.isdigit, "$Revision$")
print __version__

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        mfile = sys.argv[1]
    else:
        mfile = './main.py'

    DebugDump()

    if sys.platform == 'win32':
        fo = open(os.path.join(home, "python_out.txt"), "w")
        sys.stdout = fo
        fe = open(os.path.join(home, "python_err.txt"), "w")
        sys.stderr = fe


    execfile(mfile)

    if sys.platform == 'win32':
        fo.close()
        fe.close()
