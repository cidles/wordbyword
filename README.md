Description
-----------
WordByWord is a simple vocabulary trainer developed by Vera Ferreira, 
Peter Bouda and Ricardo Filipe at CIDLeS with the support of the
Foundation for Endangered Languages. 
WordByWord takes an ordered list of words in two languages and presents
you the words in random order. You may guess each word and then 
display the solution. WordByWord supports several modes for learning: 
you may just display the words, answer multiple choice questions or 
input the correct translation for the given word.
WordByWord uses YAML input files and is based on the Qt Framework. The
program is written in Python. So WordByWord is platform independant.
See the screenshots on the side to see WordByWord running
on a desktop and on the tablet.

The software is licensed under the GNU General Public License (see 
LICENSE file).



Requirements
------------
You need to install the following packages to run WordByWord from the source code:

- Python
- PyQt
- PyYAML (is included in the Maemo download package)

This package contains the Python source of WordByWord (and for Maemo a
copy of PyYAML). So everything is included to start the program on any
platform, including the Nokia N810 internet tablet.

Unpack the package and change into the created directory:

$ tar xzf wordbyword-1.0.0.tar.gz
$ cd wordbyword-1.0.0

Then, to start the program:

$ python wordbyword.py


Download
--------

- Windows setup: wordbyword-1.0.0.exe
- TAR.GZ for all other platforms: wordbyword-1.0.0.tar.gz
- TAR.GZ package for Maemo: wordbyword-maemo-0.2.0.tar.gz


Usage
-----

Sample files for vocabulary learning included in the package:

- Minderico for Portuguese speakers
- Portuguese for German speakers
- Russian for German speakers

Just open the files inside the "courses" folder and
see WordByWord in action.
The sample file shows how lessons and words are organized in YAML,
you may extend the file or write new YAML files according to the format
in the sample file. 


Site and contact
----------------
The website of this project is:

http://media.cidles.eu/labs/wordbyword/

If you have any questions or ideas about WordByWord just write an email
to:

pbouda@cidles.eu

