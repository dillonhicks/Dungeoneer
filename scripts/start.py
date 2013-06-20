"""


"""
__author__ = 'Dillon Hicks'
__version__ = ('0', '1', 'b')

# Most used imports
import sys
import os

from dungeoneer.gui import MainWindow 

# Version check for Python 2.6 or higher.  Just raise a warning on a
# version number < 2.6, an exit would seems a little extreme since
# there are workarounds for using lower version of the python
# interperater with newer code.
if sys.version_info < (2, 6):
    raise RuntimeWarning("""This code was designed to run with 
Python 2.6. Beware that this code may misbehave and cause errors if
not run under a compatible interperater version.""") 

# Check for PyQt4 using a try/except block looking for an
# ImportError. An import error will indicate that the PyQt4 package is
# not installed, and this GUI will not be able to function.  If this
# is the case, print an error and exit.
try:
    from PyQt4 import QtCore
    from PyQt4.QtGui import *
    from PyQt4.Qt import *
except(ImportError):
    print("""ERROR: The MyEdit GUI uses PyQt4, but there does not
appear to be a PyQt4 installation on this computer.  If you have
installed PyQt4, you may wish to change the your .bashrc PYTHONPATH
variable to point to the site of your PyQt4 installation or reinstall
PyQt4.""")
    print('Exiting...')
    raise SystemExit(1)

# As with the Python version check, this is a sanity check to alert
# the user that there version of PyQt could be incompatible with this
# version if it is a lower version. Raise an error on a
if QtCore.PYQT_VERSION_STR < '4.6.0':
    raise RuntimeWarning("""This code was designed to run with PyQt
4.6. Beware that this code may misbehave and cause errors if not
exectued with compatible PyQt version.""") 


# Entry point for the application. This is the Python equivalent of
# the main() function typically seen in C, C++, C#, Java, etc..
if __name__ == "__main__":
    # Initializes the PyQt back-end libraries
    app = QApplication(sys.argv)
    # Create an instance of the MainWindow class.
    appWindow = MainWindow()
    # Tell appWindow to be visible when app is executed.
    appWindow.show()
    # Start the GUI Loop, which executes until the appWidow object is
    # closed/destroyed.
    sys.exit(app.exec_())      

