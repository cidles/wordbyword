#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ricardo Filipe

import sys
import os
import yaml

def main():
	args = sys.argv

	data_for_yml = {}
	dict_vocabulary = {"title": "Portuguese - Minderico", "langtts": "pt-pt"}
	dict_lessons = {}
	
	for path in args[1:]:
		current_lesson = {}
		current_lesson_content = {}

		# Read File
		filename = os.path.basename(path)
		filename = filename.split(".csv")[0]
		file_object = open(path, "r")
		file_content = file_object.read()

		file_content_lines = file_content.split("\n")

		for line in file_content_lines:
			if line != "":
				word_pair = line.split(";")
				current_lesson_content[word_pair[0]] = word_pair[1]

		dict_lessons[filename] = current_lesson_content

	dict_vocabulary["lessons"] = dict_lessons
	data_for_yml["vocabulary"] = dict_vocabulary
	
	with open('result.yml', 'w') as yaml_file:
		yaml_file.write(yaml.safe_dump(data_for_yml, default_flow_style=False, allow_unicode=True, encoding='utf-8', default_style='"'))

if __name__ == "__main__":
	main()