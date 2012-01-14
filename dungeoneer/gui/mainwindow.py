from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.Qt import *

from dungeoneer.gui.board import BoardWidget, CreatePieceDialog

# This path is valid for EECS and ITTC linux installs, as well as most
# default installations of Fedora.
ICON_DIR_PATH = '/usr/share/icons/gnome/24x24/actions'
def loadIcon(iconName):
    iconPath = ICON_DIR_PATH + '/' + iconName + '.png'
    if os.path.exists(iconPath):
        return QIcon(iconPath)
    else:
        return QIcon()


APPLICATION_NAME = 'D&D Board Visualizer'
ABOUT_INFORMATION = """
Created By: Dillon Hicks (2011)
Written in Python using PyQT4 GUI Libraries
"""
        
class MainWindow(QMainWindow):
    """
    Totally Lame and Standard Main GUI Window
    """
    
    def __init__(self):
        ### Global QMainWindow Widget Setup ###

        # Initialize the base Window class to give the proper
        # functionality.  Some programming languages do this
        # automatically, but in Python you must explicitly call the
        # constructor of the class. Python supports multiple
        # inheritance, so this allows you to specify in which order
        # the multiple base classes are inherited.
        QMainWindow.__init__(self)

        # Window Wide Settings : Setting up the Window such that it
        # has a starting size of 850x620 pixels, with a minimum size
        # of 640x480 pixels. The contents margins specifies the number
        # of pixels of padding between the top, left, right, and
        # bottom boarders and the widgets residing within the Window
        # widget.
        self.setWindowTitle(APPLICATION_NAME)
        self.resize(850,620)
        self.setMinimumSize(640,480)
        self.setContentsMargins(0, 0, 0, 0)

        ### Global Editor Variables ###
        


        ### Child Widget Setup ###

        # Central Board Widget
        self.board = BoardWidget(self)

        ############################################################
        # Main Menu:
        #
        # The Main Menu is located directly below the Title Bar within
        # the window. It holds all of the possible actions that can be
        # taken to edit text within the editor.
        ############################################################

        # Copy the reference to the builtin QMainWindow's QMenuBar to
        # a variable that is easier to use and read.
        mainMenu = self.menuBar()
        
        # File Menu
        fileMenu = mainMenu.addMenu('&File')
        fileOpen = fileMenu.addAction('&Open')

        fileMenu.addSeparator()

        fileClose = fileMenu.addAction('Close')
        fileCloseAll = fileMenu.addAction('Close All')

        fileMenu.addSeparator()

        fileSave = fileMenu.addAction('&Save')
        fileSaveAs = fileMenu.addAction('S&ave As')

        fileMenu.addSeparator()
        filePrint = fileMenu.addAction('&Print')

        fileMenu.addSeparator()
        fileExit = fileMenu.addAction('&Exit')
        
        # Edit Menu
        editMenu = mainMenu.addMenu('&Edit')

        # Tools Menu
        toolsMenu = mainMenu.addMenu('T&ools')
        toolsNewPiece = toolsMenu.addAction('Create New Piece')

        # Window Menu
        windowMenu = mainMenu.addMenu('Window')

        # Help Menu
        helpMenu = mainMenu.addMenu('&Help')
        helpAbout = helpMenu.addAction('About')



        ##################################################
        # Signals
        # 
        # Note that this is only for static connections between
        # certian signals and their handler functions. Sometimes we
        # will need to have a way to connect or reconnect a signal
        # from a widget to a common handler function(s). 
        # See: switchCurrentFileEdit() for an example.
        ##################################################
        


        # Shows the totally standard "About" dialog when the menu
        # option help->about is clicked.
        self.connect(helpAbout,
                     QtCore.SIGNAL('activated()'),
                     self.showAboutApplicationDialog)
        
        self.connect(toolsNewPiece,
                     QtCore.SIGNAL('activated()'),
                     self.showCreatePieceDialog)
            
        ##################################################
        # Layout
        ##################################################
        
        self.setCentralWidget(self.board)


    def showAboutApplicationDialog(self):
        """
        Display the about message box with the typical BS.
        """
        QMessageBox.about(self, APPLICATION_NAME + ' About', ABOUT_INFORMATION )
        
        
    def showCreatePieceDialog(self):
        dlg = CreatePieceDialog(self)
        dlg.exec_()
        

    def saveFileAs(self):
        """
        Save As just renames the file, updates the new name in the
        FileTextEdit object instance and then executes a normal save
        with :func:saveFile().
        """
        # Open a filedialog with the "Save As" caption.
        saveFileName = str(QFileDialog.getSaveFileName(self, 'Save As...'))
        # Update the instance file name
        self.currentFileEdit.fileName = saveFileName
        # Save the file
        self.saveFile()


    def showOpenFileDialog(self):
        """
        Displays the file open dialog to select a file.
        """
        fileName = str(QFileDialog.getOpenFileName(self, 'Open Plain Text File'))
        # While this may have harsh reactions to some, there are
        # multiple values that are equate to false in boolean
        # expression, an incomplete list is:
        # ---------------------
        # None 
        # ''    (Empty String)
        # 0 
        # []    (Empty List)
        # (,)   (Empt Tuple) 
        # False (Duh)
        # ----------------------
        # fileName should be string, if it is an empty string the user did not 
        # input any file to open.
        if fileName:
            self.__loadTextEditWithFileText(fileName)




    def updateStatusBar(self):
        """

        """
        pass

