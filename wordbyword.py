#!/usr/bin/env pythonw
# Copyright 2009 Peter Bouda

import os, sys
sys.path.append('lib')
import yaml
import random
import hashlib
from PyQt4 import QtCore, QtGui

# check for availabe audio modules
audio_module = 'none'

try:
    from PyQt4.phonon import Phonon
    audio_module = 'phonon'
except:
    print >>sys.stderr, "no supported audio module found"
    

def main():
    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setApplicationName("WordByWord")

    qtTranslator = QtCore.QTranslator()
    qtTranslator.load("qt_" + unicode(QtCore.QLocale.system().name()), QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTranslator)

    myappTranslator = QtCore.QTranslator()
    myappTranslator.load("wordbyword_" + unicode(QtCore.QLocale.system().name()))
    app.installTranslator(myappTranslator)

    MainWindow = WordByWordWindow()
    MainWindow.show()
    sys.exit(app.exec_())

class WordByWordObject:
    def __init__(self,filename):
        self.yml = yaml.load(open(filename, "r"))
        self.currentLesson = None
        self.currentWordIndex = None
        self.currentWordCount = 0

    def setCurrentLesson(self, lesson):
        self.currentLesson = lesson
        self.lessonWords = []
        self.lessonSolutions = []
        self.currentWordCount = 0
        for word in self.yml['vocabulary']['lessons'][lesson].keys():
            self.lessonWords.append(word)
            self.currentWordCount = self.currentWordCount +1 
        random.shuffle(self.lessonWords)
        for word in self.lessonWords:
            self.lessonSolutions.append(self.yml['vocabulary']['lessons'][lesson][word])
        self.currentWordIndex = 0

    def nextWord(self):
        if self.currentWordIndex+1 < self.currentWordCount:
            self.currentWordIndex = self.currentWordIndex + 1

    def multiplechoice(self):
        ret = [ self.currentSolution() ]
        length = 3
        if self.currentWordCount < 3:
            length = self.currentWordCount
        while len(ret) < length:
            i = random.randint(0, self.currentWordCount - 1)
            word = self.lessonSolutions[i]
            if not word in ret:
                ret.append(word)
        random.shuffle(ret)
        return ret

    def prevWord(self):
        if self.currentWordIndex > 0:
            self.currentWordIndex = self.currentWordIndex - 1

    def lessonTitles(self):
        ret = self.yml['vocabulary']['lessons'].keys()
        ret.sort()
        return ret

    def currentSolution(self):
        return self.lessonSolutions[self.currentWordIndex]

    def currentWord(self):
        return self.lessonWords[self.currentWordIndex]

    def langtts(self):
        return self.yml['vocabulary']['langtts']

class WordByWordWindow(QtGui.QMainWindow):
    """The main window of the WordByWord application."""
    
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.wbwObject = None
        self.media = None
        self.coursepath = None
        self.radiobuttonsSolution = None 
        # Play mp3 on Windows and Mac and ogg elsewhere
        if os.name == 'nt' or os.name == 'mac' or os.name == 'posix':
            self.audiotype = "mp3"
        else:
            self.audiotype = "ogg"
        print >>sys.stderr, "Play audio type %s" % self.audiotype

        self.setObjectName("MainWindow")
        self.setWindowTitle("WordByWord")
        fontsizelabel = 16
        if os.environ.has_key("OSSO_PRODUCT_NAME"):
            fontsizelabel = 24
        self.setStyleSheet("QMainWindow { background: white url(background.png); background-repeat: repeat-x; } \
                            QPushButton { background: white; } \
                            QLabel#labelDisplayArea { font-family: serif; color:blue; font-size:%spx; font-weight:bold; } \
                            QLabel#labelSolution { font-family: serif; color:blue; font-size:%spx; font-weight:bold; }" % (fontsizelabel, fontsizelabel))
        self.resize(696, 396)
        self.hboxLayoutWidget = QtGui.QWidget(self)
        self.hboxLayout = QtGui.QHBoxLayout(self.hboxLayoutWidget)
        self.hboxLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)

        self.hboxLayout.addWidget(self.controlButtons())
        self.hboxLayout.addWidget(self.displayArea())

        self.hboxLayoutWidget.setLayout(self.hboxLayout)
        self.setCentralWidget(self.hboxLayoutWidget)

        self.initMenu()
        self.initSignals()
        self.actionModeDisplayOnly.setChecked(True)
        filename = ''
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        elif (os.path.exists('start.ini')):
            startfile = open('start.ini', 'r')
            filename = startfile.readline().rstrip('\n')
        if filename != '' and os.path.exists(filename):
            self.wbwObject = WordByWordObject(filename)
            self.initLessons()
            self.showCurrentWord()
            self.coursepath = os.path.dirname(os.path.abspath(filename))

    def displayArea(self):
        widgetDisplayArea = QtGui.QWidget(self)
        vboxLayoutDisplayArea = QtGui.QVBoxLayout(widgetDisplayArea)
        #vboxLayoutDisplayArea.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        vboxLayoutDisplayArea.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        vboxLayoutDisplayArea.setContentsMargins(50, QtGui.QStyle.PM_LayoutTopMargin, QtGui.QStyle.PM_LayoutRightMargin, QtGui.QStyle.PM_LayoutBottomMargin)


        self.labelDisplayArea = QtGui.QLabel(self.tr("Please open a file"))
        self.labelDisplayArea.setFixedWidth(400)
        self.labelDisplayArea.setWordWrap(True)
        self.labelDisplayArea.setObjectName("labelDisplayArea")
        #self.labelDisplayArea.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        vboxLayoutDisplayArea.addWidget(self.labelDisplayArea)

        self.widgetDisplayAdditional = QtGui.QWidget(widgetDisplayArea)
        vboxLayoutDisplayAdditional = QtGui.QVBoxLayout(self.widgetDisplayAdditional)
        self.widgetDisplayAdditional.setLayout(vboxLayoutDisplayAdditional)
        vboxLayoutDisplayArea.addWidget(self.widgetDisplayAdditional)
 
        self.labelSolution = QtGui.QLabel("")
        self.labelSolution.setWordWrap(True)
        self.labelSolution.setObjectName("labelSolution")
        vboxLayoutDisplayArea.addWidget(self.labelSolution)
        self.labelCorrectOrNot = QtGui.QLabel("")
        self.labelCorrectOrNot.font().setPixelSize(14)
        vboxLayoutDisplayArea.addWidget(self.labelCorrectOrNot)
        self.buttonListen = QtGui.QPushButton(self.tr("Read Solution"))
        self.buttonListen.setDisabled(True)
        vboxLayoutDisplayArea.addWidget(self.buttonListen)

        widgetDisplayArea.setLayout(vboxLayoutDisplayArea)
        return widgetDisplayArea

    def controlButtons(self):
        widgetControlButtons = QtGui.QWidget(self)
        vboxLayout = QtGui.QVBoxLayout(widgetControlButtons)
        vboxLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.buttonOpen = QtGui.QPushButton(self.tr("Open"), self)
        vboxLayout.addWidget(self.buttonOpen)
        self.buttonPrev = QtGui.QPushButton(self.tr("Previous"), self)
        self.buttonPrev.setEnabled(False)
        vboxLayout.addWidget(self.buttonPrev)
        self.buttonNext = QtGui.QPushButton(self.tr("Next"), self)
        self.buttonNext.setEnabled(False)
        vboxLayout.addWidget(self.buttonNext)
        self.buttonSolution = QtGui.QPushButton(self.tr("Solution"), self)
        self.buttonSolution.setEnabled(False)
        vboxLayout.addWidget(self.buttonSolution)
        widgetControlButtons.setLayout(vboxLayout)
        widgetControlButtons.setFixedSize(150,350)
        return widgetControlButtons

    def initMenu(self):
        # Open
        self.actionOpenFile = QtGui.QAction(self.tr("Open File..."), self)
        self.actionOpenFile.setObjectName("actionOpenFile")
        # Quit
        self.actionQuit = QtGui.QAction(self.tr("Quit"), self)
        self.actionQuit.setMenuRole(QtGui.QAction.QuitRole)
        self.actionQuit.setObjectName("actionQuit")

        fileMenu = self.menuBar().addMenu(self.tr("File"))
        fileMenu.addAction(self.actionOpenFile)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actionQuit)

        # Modes
        self.actiongroupModes = QtGui.QActionGroup(self)
        self.actionModeDisplayOnly = QtGui.QAction(self.tr("Display only"), self.actiongroupModes)
        self.actionModeDisplayOnly.setCheckable(True)
        self.actiongroupModes.addAction(self.actionModeDisplayOnly)
        self.actionModeMultipleChoice = QtGui.QAction(self.tr("Multiple choice"), self.actiongroupModes)
        self.actionModeMultipleChoice.setCheckable(True)
        self.actiongroupModes.addAction(self.actionModeMultipleChoice)
        self.actionModeInputField = QtGui.QAction(self.tr("Input field"), self.actiongroupModes)
        self.actionModeInputField.setCheckable(True)
        self.actiongroupModes.addAction(self.actionModeInputField)
        self.actiongroupModes.setExclusive(True)
        modesMenu = self.menuBar().addMenu(self.tr("Mode"))
        modesMenu.addActions(self.actiongroupModes.actions())
        #self.menuModes.addActions(self.actiongroupModes.actions())

        # Lessons
        actionLessons = QtGui.QAction(self.tr("no file loaded"), self)
        actionLessons.setDisabled(True)
        self.menuLessons = self.menuBar().addMenu(self.tr("Lesson"))
        self.menuLessons.addAction(actionLessons)

        # About
        self.actionAboutWordByWord = QtGui.QAction(self.tr("About WordByWord"), self)
        self.actionAboutWordByWord.setMenuRole(QtGui.QAction.AboutRole)	
        self.actionAboutWordByWord.setObjectName("actionAboutWordByWord")

        aboutMenu = self.menuBar().addMenu(self.tr("About"))
        aboutMenu.addAction(self.actionAboutWordByWord)

    def initSignals(self):
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("triggered()"), self.close)
        QtCore.QObject.connect(self.actionOpenFile, QtCore.SIGNAL("triggered()"), self.fileBrowser)
        QtCore.QObject.connect(self.actionAboutWordByWord, QtCore.SIGNAL("triggered()"), self.aboutDialog)
        QtCore.QObject.connect(self.buttonOpen, QtCore.SIGNAL("clicked()"), self.fileBrowser)
        QtCore.QObject.connect(self.buttonPrev, QtCore.SIGNAL("clicked()"), self.prevWord)
        QtCore.QObject.connect(self.buttonNext, QtCore.SIGNAL("clicked()"), self.nextWord)
        QtCore.QObject.connect(self.buttonSolution, QtCore.SIGNAL("clicked()"), self.showSolution)
        QtCore.QObject.connect(self.buttonListen, QtCore.SIGNAL("clicked()"), self.listenSolution)
        QtCore.QObject.connect(self.actionModeDisplayOnly, QtCore.SIGNAL("changed()"), self.setMode)
        QtCore.QObject.connect(self.actionModeMultipleChoice, QtCore.SIGNAL("changed()"), self.setMode)
        QtCore.QObject.connect(self.actionModeInputField, QtCore.SIGNAL("changed()"), self.setMode)
        QtCore.QMetaObject.connectSlotsByName(self)

    def aboutDialog(self):
        about = QtGui.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setWindowTitle(self.tr("About WordByWord"))
        about.setText(self.tr("""<b>WordByWord 1.0.0</b><br/>
            vocabulary trainer developed by Vera Ferreira, Peter Bouda and Ricardo Filipe at <a href=\"http://cidles.eu\">CIDLeS</a><br/>
            <br/>
            Supported by <a href=\"http://www.ogmios.org\">Foundation for Endangered Languages</a><br/>
            <br/>
            All rights reserved. See LICENSE file for details.<br/>
            <br/>
            For more information visit the website:<br/>
            <a href=\"http://media.cidles.eu/labs/wordbyword\">http://media.cidles.eu/labs/wordbyword/</a><br/>
            <br/>Audio files were produced by:
            <ul>
                <li>Minderico: Elsa Nogueira, Rita Pedro, Pedro Manha (Minderico speakers)</li>
                <li>Portuguese: <a href=\"http://www.linguatec.de/products/tts/voice_reader/vrs\">Linguatec's Voice Reader Studio</a></li>
                <li>Russian: <a href=\"http://www.linguatec.de/products/tts/voice_reader/vrs\">Linguatec's Voice Reader Studio</a></li>
            </ul>
            <br/>
            """))
        about.exec_()

    def prevWord(self):
        self.wbwObject.prevWord()
        self.setDisplayArea()
        self.buttonListen.setDisabled(True)

    def nextWord(self):
        self.wbwObject.nextWord()
        self.setDisplayArea()
        self.buttonListen.setDisabled(True)

    def showSolution(self):
        s = self.wbwObject.currentSolution()
        h = hashlib.md5(s.encode("utf-8")).hexdigest()
        if os.path.exists("%s/audio/%s/%s.%s" % (self.coursepath, self.wbwObject.langtts(), h, self.audiotype)) and audio_module != 'none':
            self.buttonListen.setDisabled(False)
        self.labelSolution.setText(s)
        if self.currentMode > 1:
            solution = ""
            if self.currentMode == 2:
                for radiobutton in self.radiobuttonsSolution:
                    if radiobutton.isChecked():
                        solution = radiobutton.text()
            if self.currentMode == 3:
                solution = self.inputfieldSolution.text()
            if solution == self.wbwObject.currentSolution():
                self.labelCorrectOrNot.setText(self.tr("This was the correct answer!"))
            else:
                self.labelCorrectOrNot.setText(self.tr("Sorry, wrong answer :-("))

    def listenSolution(self):
        s = self.wbwObject.currentSolution()
        h = hashlib.md5(s.encode("utf-8")).hexdigest()
        mp3 = "%s/audio/%s/%s.%s" % (self.coursepath, self.wbwObject.langtts(), h, self.audiotype)
        if os.path.exists(mp3) and audio_module != 'none':
            if not self.media:
                self.media = Phonon.MediaObject(self)
                audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
                Phonon.createPath(self.media, audioOutput)
            self.media.setCurrentSource(Phonon.MediaSource(os.path.abspath(mp3)))
            self.media.play()

    def setMode(self):
        if self.actionModeDisplayOnly.isChecked():
            self.currentMode = 1
        elif self.actionModeMultipleChoice.isChecked():
            self.currentMode = 2
        elif self.actionModeInputField.isChecked():
            self.currentMode = 3
        self.setDisplayArea()
        self.buttonListen.setDisabled(True)

    def fileBrowser(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, self.tr("Select File"), "", "YAML (*.yml)")
        filename = unicode(filename)
        if filename != '':
            self.wbwObject = WordByWordObject(filename)
            self.initLessons()
            self.showCurrentWord()
            self.coursepath = os.path.dirname(os.path.abspath(filename))

    def initLessons(self):
        lessons = self.wbwObject.lessonTitles()
        self.menuLessons.clear()
        self.actiongroupLessons = QtGui.QActionGroup(self.menuLessons)
        for lesson in lessons:
            actionLesson = QtGui.QAction(lesson, self.actiongroupLessons)
            actionLesson.setCheckable(True)
            self.actiongroupLessons.addAction(actionLesson)
            QtCore.QObject.connect(actionLesson, QtCore.SIGNAL("changed()"), self.setLesson)              
        self.menuLessons.addActions(self.actiongroupLessons.actions())
        self.actiongroupLessons.actions()[0].setChecked(True)
        self.buttonListen.setDisabled(True)

    def setNextButtonState(self):
        if self.wbwObject.currentWordIndex + 1 < self.wbwObject.currentWordCount:
            self.buttonNext.setEnabled(True)
        else:
            self.buttonNext.setEnabled(False)

    def setPrevButtonState(self):
        if self.wbwObject.currentWordIndex > 0:
            self.buttonPrev.setEnabled(True)
        else:
            self.buttonPrev.setEnabled(False)

    def setSolutionButtonState(self):
        self.buttonSolution.setEnabled(True)

    def setDisplayArea(self):
        if self.wbwObject == None:
            return
        self.labelDisplayArea.setText(self.wbwObject.currentWord())
        # delete all stuff in additional area
        has_children = True
        while has_children:
            child = self.widgetDisplayAdditional.layout().takeAt(0)
            if child == None:
                has_children = False
            else:
                child.widget().setParent(None)
        if self.currentMode == 1:
            self.labelDisplayArea.setText(self.wbwObject.currentWord())
        else:
            if self.currentMode == 2:
                words = self.wbwObject.multiplechoice()
                self.radiobuttonsSolution = []
                for word in words:
                    button = QtGui.QRadioButton(word, self.widgetDisplayAdditional)
                    self.widgetDisplayAdditional.layout().addWidget(button)
                    self.radiobuttonsSolution.append(button)
            if self.currentMode == 3:
                self.inputfieldSolution = QtGui.QLineEdit(self.widgetDisplayAdditional)
                self.inputfieldSolution.setFixedWidth(300)
                self.widgetDisplayAdditional.layout().addWidget(self.inputfieldSolution)
                
        self.labelSolution.setText("")
        self.labelCorrectOrNot.setText("")
        self.setNextButtonState()
        self.setPrevButtonState()
        self.setSolutionButtonState()

    def setLesson(self):
        for action in self.actiongroupLessons.actions():
            if action.isChecked():
                self.wbwObject.setCurrentLesson(unicode(action.text()))
        self.setWindowTitle("%s - WordByWord" % self.wbwObject.currentLesson)
        self.setDisplayArea()
      
    def showCurrentWord(self):
        pass
main()
