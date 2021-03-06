#!/usr/bin/python 
# -*- coding: utf-8 -*-

# call:
#   zotero_link.py %t

import sys
import os
import re
import datetime
import time

zotero = "zotero://127.0.0.1:23119/zotxt/select?betterbibtexkey="

def main(selection):
    txt = ""
    txt += "===== {} =====\n\n".format(selection)
    txt += "@{}\n".format(selection)
    txt += "[[{}|{}]]\n".format(zotero + selection, selection)
    print(txt)

if __name__ == "__main__":
    main(sys.argv[1])