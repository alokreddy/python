# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:30:54 2016

@author: ReddyAl
"""

def filefinder():
    extension = raw_input("Input file extension: ")
    extensions = "\\*" + extension
    _ = glob.glob( "".join([ os.getcwd(), extensions]))
    if not _:
        print "There is no file in the current working directory with the extension {}".format(extension)
    return _