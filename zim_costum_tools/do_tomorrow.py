#!/usr/bin/python 
# -*- coding: utf-8 -*-

# call:
#   to_tomorrow.py %s %n

import sys
import os
import re
import datetime
import time


# regex to remove
deleted = re.compile("(.*)~~.*~~(.*)")
empty_item = re.compile("^\*\s*$")


def create_folder_structure(notebook_path, namespace):
    """ creates new year and month folder structures, if 
    tomorrow is in the following month or year and the path 
    does not exists."""
    path = notebook_path
    for i in namespace.split(os.sep):
        if not os.path.exists(os.path.join(path, i)):
            os.mkdir(os.path.join(path, i))
            f = open(os.path.join(path, "%s.txt" % i), 'w')
            # TODO: how to get page template?
            f.write("Content-Type: text/x-zim-wiki\nWiki-Format: zim 0.4\n\n")
            f.write("====== %s ======\n" % i) #TODO: month names
            f.close()
        path = os.path.join(path, i)


def main(orig_file, notebook_path):
    new_files_content = ""
    date_found = 0
    f = open(orig_file)
    for line in f:
        if re.match("====== \w+ \d+ \w+ \d\d\d\d ======",line) and not date_found:
            # extract date and calculate tomorrow
            date = line.split(' ')
            try:
                today = time.strptime(' '.join(date[2:5]),"%d %b %Y")
                today = datetime.date(today[0],today[1],today[2])
            except ValueError:
                print "Can not parse date header"
                continue
            difference1 = datetime.timedelta(days=1)
            tomorrow = today + difference1
            date_found = 1
            line = "====== %s ======" % tomorrow.strftime("%a %d %b %Y")
        while re.match(deleted, line):
            line = re.sub(deleted, r'\1\2',line)
        if re.match(empty_item,line):
            continue
        new_files_content += line
    f.close()

    # create filename for tomorrow
    if not date_found:
        # it was not possible to extract date from date header
        # simply +1 to filename
        tmp = orig_file.split(os.sep)
        new_file_path = os.path.join(*tmp[:-1])
        orig = tmp[-1].split('.')[0]
        new_file_name = "%02d.txt" % (int(orig) + 1)
        notebook_path = ""
        sys.exit(0)
        #TODO: add header describing the problem
    else:
        new_file_path = os.path.join("Calendar",str(tomorrow.year),str("%02d"%tomorrow.month))
        new_file_name = "%02d.txt" %tomorrow.day

    new_file = os.path.join(notebook_path, new_file_path, new_file_name)

    if os.path.exists(new_file):
        f = open(new_file,'a')
        # in this case: remove 3 header lines
        new_files_content = '\n'.join(new_files_content.split('\n')[3:])
        # TODO: remove date header?
    else:
        if not os.path.exists(os.path.join(notebook_path, new_file_path)):
            create_folder_structure(notebook_path, new_file_path)
        f = open(new_file, 'w')

    f.write(new_files_content)
    f.close()
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])