#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ricardo Filipe

import sys
import os
import hashlib


def main():
	args = sys.argv
	
	for path in args[1:]:

		file_object = open(path, "r")
		file_content = file_object.read()

		file_content_lines = file_content.split("\n")

		for line in file_content_lines:
			if line != "":
				word_pair = line.split(";")
				word = word_pair[1]
				oldname = word_pair[2]
				h = hashlib.md5(word).hexdigest()
				newname = h + ".mp3"
				if os.path.exists(oldname):
					os.rename(oldname, newname)
				else:
					print "Could not find: " + oldname


if __name__ == "__main__":
	main()