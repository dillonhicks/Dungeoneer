import os

from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.Qt import *

from dungeoneer.pieces import game_pieces, game_pieces_by_name
from dungeoneer import conf

DEFAULT_GRID_SPACING = 0
DEFAULT_GRID_MARGINS = (0, 0, 0, 0)

class PieceWidget(QWidget):
    def __init__(self, parent, piece):        
        QWidget.__init__(self, parent)
        
        self.piece = piece
        
        toolTip = u''
        for attr in ('name', 'level', 'hp'):
            toolTip += '%s: %s\n' % (attr.title(), self.piece[attr])
        self.setToolTip(toolTip)
        
        self.svgItem = QSvgWidget(
            os.path.join(conf.MEDIA_PATH, self.piece.image), self)        

        self.grid = QGridLayout()
        if self.piece.type == 'terrain':
            self.grid.setSpacing(DEFAULT_GRID_SPACING)
            self.grid.setContentsMargins(*DEFAULT_GRID_MARGINS)

        self.grid.addWidget(self.svgItem, 0, 0)        
        self.setLayout(self.grid)

class AddPieceDialog(QDialog):
    def __init__(self, parent, xCoord, yCoord):

        super(AddPieceDialog, self).__init__(parent)
        self.setWindowTitle('Add Piece to (%d, %d)' % (xCoord, yCoord))
        self.grid = QGridLayout(self)        
        
        # Piece Selection
        self.piecesLabel = QLabel('Piece:')
        self.piecesComboBox = QComboBox(self)
        for piece in sorted([p.name for p in game_pieces]):
            self.piecesComboBox.addItem(piece)
            
        self.grid.addWidget(self.piecesLabel, 0, 0)
        self.grid.addWidget(self.piecesComboBox, 0, 1)

        
        # Buttons
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        self.grid.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.connect(self.buttonBox, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(self.buttonBox, SIGNAL("rejected()"),
                     self, SLOT("reject()"))

        self.setLayout(self.grid)


class CreatePieceDialog(QDialog):
    def __init__(self, parent):
        super(CreatePieceDialog, self).__init__(parent)
        self.setWindowTitle('Create New Piece')        
        self.setLayout(QFormLayout(self))

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        self.filePushButton = QPushButton('<no image selected>', self)
        self.filePushButton.setFlat(True)
        self.filePushButton.setStyleSheet("""
QPushButton {
    background-color: #FFFFFF;
}
""")

        self.layout().addRow('Name:', QLineEdit(self))

        self.layout().addRow('Image:', self.filePushButton )
        self.layout().addRow(QLineEdit(self), QLineEdit(self))
        self.layout().addRow(QLabel(''), self.buttonBox)



        self.connect(self.buttonBox, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(self.buttonBox, SIGNAL("rejected()"),
                     self, SLOT("reject()"))


        self.connect(
            self.filePushButton, SIGNAL('clicked()'),
            self.showFileDialog)

    def showFileDialog(self):
        filename = QFileDialog.getOpenFileName(
            self, 'Use Image', os.getcwd(), 'Images (*.svg)')

        if filename:
            self.filePushButton.setText(filename)
        
class ZoneWidget(QPushButton):
    def __init__(self, parent, xCoord, yCoord):
        super(ZoneWidget, self).__init__(parent)

        self.xCoord = xCoord
        self.yCoord = yCoord

        # Widget Attrs
        self.setStyleSheet("""
QPushButton {
    background-color: #DDDDDD;
    border: 1px solid black;
}

QPushButton::menu-indicator {
   image: none;
}
""")
        self.setAutoFillBackground(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFlat(True)

        # self.setContextMenuPolicy(Qt.DefaultContextMenu)
        # self.contextMenu = QMenu(self)
        
        zoneMenu = QMenu("MENU!", self)
        self.addItemAction = QAction('Add', zoneMenu)

        self.deleteItemAction = QAction('Delete', zoneMenu)
        self.deleteItemAction.setVisible(False)

        zoneMenu.addAction(self.addItemAction)
        zoneMenu.addSeparator()
        zoneMenu.addAction(self.deleteItemAction)

        self.setMenu(zoneMenu)

        self.connect(
            self.addItemAction, QtCore.SIGNAL('triggered()'), 
            self.showAddItemDialog)

        self.connect(
            self.deleteItemAction, QtCore.SIGNAL('triggered()'), 
            self.deleteItem)
                
        self.grid = QGridLayout()
        self.grid.setSpacing(DEFAULT_GRID_SPACING)
        self.grid.setContentsMargins(*DEFAULT_GRID_MARGINS)

        self.setLayout(self.grid)
        self.piece = None

    def showAddItemDialog(self):
        if self.piece:
            return

        dlg = AddPieceDialog(self, self.xCoord, self.yCoord)
        if dlg.exec_():
            name = unicode(dlg.piecesComboBox.currentText())
            piece = game_pieces_by_name[name]
            
            self.piece = PieceWidget(self, piece)
            self.layout().addWidget(self.piece, 0, 0)

            self.addItemAction.setVisible(False)
            self.deleteItemAction.setVisible(True)


    def deleteItem(self):
        if not self.piece:
            return

        self.layout().removeWidget(self.piece)
        self.piece.hide()
        del self.piece
        self.piece = None

        self.addItemAction.setVisible(True)
        self.deleteItemAction.setVisible(False)




class BoardWidget(QWidget):

    def __init__(self, parent, rows=10, columns=10):
        QWidget.__init__(self, parent)
        
        # Widget Attrs
#        self.setStyleSheet("QWidget {background-color: #0FFFFF}")
        self.resize(800,600)
        self.setAutoFillBackground(True)

        # Layouts
        self.grid = QGridLayout(self)
        self.grid.setSpacing(DEFAULT_GRID_SPACING)
        self.grid.setContentsMargins(*DEFAULT_GRID_MARGINS)
        self.setLayout(self.grid)
        
        for x in range(columns):
            for y in range(rows):
                zone = ZoneWidget(self, x, y)        
                self.grid.addWidget(zone, x, y)
        

    # def setFillColor(self, Red=100, Green=170, Blue=220):
    #     fillColor = QColor(Red,Green,Blue)
    #     backgroundPixmap = QPixmap(self.size())
    #     backgroundPixmap.fill(fillColor)
    #     self.backgroundLabel.setPixmap(backgroundPixmap)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # Initializes the PyQt back-end libraries
    # Create an instance of the MainWindow class.
    appWindow = BoardWidget(None)

    # Tell appWindow to be visible when app is executed.
    appWindow.show()
    app.exec_()




