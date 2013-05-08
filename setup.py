#!/usr/bin/env python

#
# WordByWord - a vocabulary trainer
# Copyright (c) 2009 Peter Bouda
#
# WordByWord is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# WordByWord is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, os
import glob
import re
from distutils.core import setup

# build targets
(DEFAULT, WINDOWS, MAEMO) = range(3)
target = DEFAULT

# import the gpodder module locally for module metadata
sys.path.insert(0, 'src')
import wordbyword

# if we are running "setup.py sdist", include all targets (see below)
building_source = ('sdist' in sys.argv)

# build target
if 'TARGET' in os.environ:
    if os.environ['TARGET'].strip().lower() == 'maemo':
        target = MAEMO
    if os.environ['TARGET'].strip().lower() == 'windows':
        target = WINDOWS

target_dir = 'share'
if target == MAEMO:
  target_dir = '/opt'

# files to install
inst_desktop = [ 'data/wordbyword.desktop' ]
inst_desktop_maemo = [ 'data/maemo/wordbyword.desktop' ]
inst_icon_scalable = [ 'data/icons/scalable/wordbyword.png' ]
inst_background = [ 'data/background.png' ]
inst_courses_yml = glob.glob('data/courses/*.yml')
inst_courses_audio_ru_ogg = glob.glob('data/courses/audio/ru-ru/*.ogg')
inst_courses_audio_pt_ogg = glob.glob('data/courses/audio/pt-pt/*.ogg')
inst_courses_audio_ru_mp3 = glob.glob('data/courses/audio/ru-ru/*.mp3')
inst_courses_audio_pt_mp3 = glob.glob('data/courses/audio/pt-pt/*.mp3')

# data files
data_files = [
]

# packages
packages = [
#  'wordbyword',
]

# target-specific installation data files
if target == DEFAULT or building_source:
    data_files += [
      ('share/applications', inst_desktop),
      (target_dir + '/wordbyword/courses', inst_courses_yml),
    ]

if target == DEFAULT or target == MAEMO or building_source:
    data_files += [
      (target_dir + '/wordbyword/courses/audio/ru-ru', inst_courses_audio_ru_ogg),
      (target_dir + '/wordbyword/courses/audio/pt-pt', inst_courses_audio_pt_ogg)
    ]

if target == WINDOWS or building_source:
    data_files += [
      ('share/wordbyword/courses/audio/ru-ru', inst_courses_audio_ru_mp3),
      ('share/wordbyword/courses/audio/pt-pt', inst_courses_audio_pt_mp3)
    ]

if target == MAEMO:
    data_files += [
      ('share/applications/hildon', inst_desktop_maemo),
      ('share/icons/hicolor/scalable/hildon', inst_icon_scalable),
      (target_dir + '/wordbyword/courses', inst_courses_yml),
    ]
    packages += [
      'yaml',
    ]

# search for translations and repare to install
translation_files = []
for qmfile in glob.glob('data/locale/*.qm'):
    qmdir = os.path.dirname(qmfile).replace('data', target_dir + '/wordbyword')
    translation_files.append((qmdir, [qmfile]))


author, email = re.match(r'^(.*) <(.*)>$', wordbyword.__author__).groups()

setup(
  name             = 'wordbyword',
  version          = wordbyword.__version__,
  package_dir      = { '':'src' },
  packages         = packages,
  description      = 'WordByWord Vocabulary Trainer',
  long_description = 'WordByWord is a simple vocabulary trainer that takes an ordered list of words in two languages and presents you the words in random order. You may guess each word and then display the solution. WordByWord supports several modes for learning: you may just display the words, answer multiple choice questions or input the correct translation for the given word.',
  author           = author,
  author_email     = email,
  url              = wordbyword.__url__,
  scripts          = glob.glob('bin/*'),
  data_files       = data_files + translation_files
)


#setup(name='wordbyword',
#version='0.2.0',
#author='Peter Bouda',
#author_email='p.bouda@gmx.de',
#url='http://www.peterbouda.de/downloads/wordbyword',
#description='WordByWord Vocabulary Trainer',
#long_description='WordByWord is a simple vocabulary trainer that takes an ordered list of words in two languages and presents you the words in random order. You may guess each word and then display the solution. WordByWord supports several modes for learning: you may just display the words, answer multiple choice questions or input the correct translation for the given word. Learning the lessons included in the packages you may also listen to the pronunciation of each word.',
#data_files=[('courses' ,['src/courses/*.yml']), ('courses/audio/ru-ru', ['src/courses/audio/ru-ru/*.mp3', 'src/courses/audio/ru-ru/*.ogg']), ('courses/audio/pt-pt', ['src/courses/audio/pt-pt/*.mp3', 'src/courses/audio/pt-pt/*.ogg'])])
