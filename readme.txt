Description
-----------
WordByWord is a free, open source, easy-to-use multimedia vocabulary 
trainer developed by Vera Ferreira, Peter Bouda, and Ricardo Filipe at 
CIDLeS with the support of the Foundation for Endangered Languages. 

WordByWord takes an ordered list of words in two languages, organized 
in lessons, and presents the words in random order. It also allows the 
user to listen to the pronunciation of the words in the target language. 
The main language course in WordByWord is Minderico for Portuguese 
speakers (WordByWord - Aprender Minderico) but the program is flexible 
enough to easily adapt to other languages (as you can see in the sample 
courses of Portuguese and Russian for German speakers included in the 
package).

The exercises are presented in the source language (for instance 
Portuguese in the case of WordByWord - Aprender Minderico) and the 
answers should be given in the target language (for instance Minderico 
in WordByWord - Aprender Minderico). For each lesson there are three 
modes of interaction with different difficulty levels: multiple choice 
questions, a fill out mode (to input the correct translation for the word 
shown and practice writing), and a display mode (a word in the source 
language is shown and the user is supposed to say the word in the target 
language aloud – an excercise to train the pronunciation). 

The audio files for Minderico were created by three Minderico speakers 
(Elsa Nogueira, Rita Pedro, and Pedro Manha). The audio files for 
Portuguese and Russian were created with Linguatec Voice Reader Studio.

WordByWord uses YAML input files and is based on the Qt Framework. The 
program is written in Python. So WordByWord is platform independent.

The software is licensed under the GNU General Public License (see 
LICENSE file).


Installation
------------
Windows users only need to download and install the setup package 
available below. To install WordByWord v1.0.0 you need to uninstall any 
previous versions beforehand.

To run WordByWord from the source code you need to install the following 
packages :

- Python
- PyQt (you might need to also do a "apt-get install phonon*" to install 
Phonon)
- PyYAML 


Download
--------

- Windows setup: wordbyword-1.0.0.msi
- Source code package for all platforms: wordbyword-1.0.0.tar.gz


Usage
-----

On Windows you just install the software by starting the .msi package 
you downloaded above. An entry in the start menu will automatically be 
created. 

For Linux and Mac unpack the source code package and change into the 
created directory:

$ tar xzf wordbyword-1.0.0.tar.gz
$ cd wordbyword-1.0.0

Then, to start the program:

$ python wordbyword.py


Course files for vocabulary learning included in the program:

- Minderico for Portuguese speakers
- Portuguese for German speakers (sample file)
- Russian for German speakers (sample file)

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

vferreira@cidles.eu or pbouda@cidles.eu