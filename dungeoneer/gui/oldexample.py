class Location:
    """
        Specialized location class that on top of normal x,y,z coords,
        has a level and a zone. Example, (First Floor, Living Room, 10.4, 12.3, 8.0)
    """ 
    def __init__(self, level = "no", zone = "where", x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.zone = zone
        self.level = level

    def getXYZ(self):
        """Returns the coords X, Y, Z as tuple"""
        return (self.x, self.y, self.z)
    
    def getXY(self):
        return (self.x, self.y)
    
    def getZone(self): 
        """Returns Zone"""
        return self.zone
    
    def getLevel(self):
        """Retuns level"""
        return self.level
    
    def getLevelZone(self):
        return '%s - %s'%(self.level, self.zone)

    def __str__(self):
        """ Returns 'level, zone, x, y, z'"""
        temp = self.getLevel() + ", "
        temp +=  self.getZone() + ", "
        temp += str(self.getXY())
        return temp
        
        def __eq__(self, loc):
                return bool(self.x == loc.x and self.y == loc.y
                                        and self.zone == loc.zone and self.level == loc.level)

class Zone(QWidget):
    """Zone Widget Class capable of drawing a graphical widget based version of the zone."""
    def __init__(self, name = 'nameless zone' , size = (100,100), position = (0,0), parent = None):
        #Widget Wide Settings
        QWidget.__init__(self,parent)           
        self.__name__ = name  
        self.resize(*size)
        self.setMaximumSize(*size)
        self.position = position
        self.setLayout(QGridLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)       
                
        #Infomation Settings
        self.setToolTip("%s<br>%s,%s"%(self.__name__, self.width(), self.height()))
        
        #Used to keep track of devices.
        #Easier than getting the children of the widget.
        self.__zoneDevices = []
        
        #Background Label
        self.backgroundLabel = QLabel()
        self.setFillColor()
        
        #HighlightLabel for background mouse hover highlighting
        highlightPixmap = QPixmap(self.size())
        highlightPixmap.fill(QColor(255,255,255,40))
        self.highlightLabel = QLabel()
        self.highlightLabel.setPixmap(highlightPixmap)
        self.highlightLabel.hide()
       
        #Interior Layout Holds the Devices.     
        self.interiorLayout = QGridLayout()
        self.interiorLayout.setContentsMargins(0,0,0,0)
        self.interiorLayout.setSpacing(0)
        self.layout().addItem(QSpacerItem(self.width()-10, self.height()-10, QSizePolicy.Expanding, QSizePolicy.Expanding),1,1)
        #Add the background/highlight behind the interior widget that holds the devices.
        self.layout().addWidget(self.backgroundLabel, 1, 1)
        self.layout().addWidget(self.highlightLabel, 1, 1)
        layoutWidget = QWidget()
        layoutWidget.resize(Device.DEFAULT_WIDTH, Device.DEFAULT_HEIGHT)
        layoutWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.interiorLayout.addWidget(layoutWidget,0,0, layoutWidget.width(), layoutWidget.height())
        self.interiorLayout.addWidget(layoutWidget, self.width()-layoutWidget.width(), self.height() -layoutWidget.height()
                                      , layoutWidget.width(), layoutWidget.height())
        self.layout().addLayout(self.interiorLayout, 1, 1)
        self.layout().setColumnStretch(1,20)
        self.layout().setRowStretch(1,20)
        
                
        #Creating Boarders 0 and 1
        hBorderPixmap = QPixmap(self.size().width(), 2)
        hBorderPixmap.fill(QColor(0,0,0))        
        vBorderPixmap = QPixmap(2, self.size().height())
        vBorderPixmap.fill(QColor(0,0,0))        
        hBorder = QLabel()
        hBorder.setPixmap(hBorderPixmap)
        vBorder = QLabel()
        vBorder.setPixmap(vBorderPixmap)   
        self.layout().addWidget(hBorder, 2,0,1,3)
        self.layout().addWidget(vBorder, 0,2,3,1)
        
        #Creating Boarders 2 and 3
        hBorderPixmap = QPixmap(self.size().width(), 2)
        hBorderPixmap.fill(QColor(0,0,0))               
        vBorderPixmap = QPixmap(2, self.size().height())
        vBorderPixmap.fill(QColor(0,0,0))               
        hBorder = QLabel()
        hBorder.setPixmap(hBorderPixmap)
        vBorder = QLabel()
        vBorder.setPixmap(vBorderPixmap)        
        self.layout().addWidget(hBorder, 0,0,1,3)
        self.layout().addWidget(vBorder, 0,0,3,1)
    
        #Shrink Boarder to not take any more room than needed.
        self.layout().setColumnStretch(0,-1)
        self.layout().setRowStretch(0,-1)
        self.layout().setColumnStretch(2,-1)
        self.layout().setRowStretch(2,-1)
        
        #Menu
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.contextMenu = QMenu(self)
                       
        zoneMenu = QMenu(self.getName(), self.contextMenu)
        addDevice = QAction('Add A Device', zoneMenu)
        turnOffDevices = QAction('Turn Off All Devices', zoneMenu)
        turnOnDevices = QAction('Turn On All Devices', zoneMenu)
        removeDevice = QAction('Remove A Device', zoneMenu)
        
        
        self.connect(addDevice, QtCore.SIGNAL('triggered()'), self.showAddDeviceDialog)
        self.connect(removeDevice, QtCore.SIGNAL('triggered()'), self.showRemoveDeviceDialog)
        self.connect(turnOffDevices, QtCore.SIGNAL('triggered()'), self.turnOffDevices)
        self.connect(turnOnDevices, QtCore.SIGNAL('triggered()'), self.turnOnDevices)
        
        zoneMenu.addAction(turnOnDevices)
        zoneMenu.addAction(turnOffDevices)
        zoneMenu.addSeparator()
        zoneMenu.addAction(addDevice)
        zoneMenu.addAction(removeDevice)
        self.contextMenu.addMenu(zoneMenu)
        self.contextMenu.addSeparator()
        #zoneMenu.addAction(QAction('Turn On All Devices', self.contextMenu))
        #self.setMenu(actionMenu)
    
    def setFillColor(self, Red=100, Green=170, Blue=220):
        fillColor = QColor(Red,Green,Blue)
        backgroundPixmap = QPixmap(self.size())
        backgroundPixmap.fill(fillColor)
        self.backgroundLabel.setPixmap(backgroundPixmap)
    
    def contextMenuEvent(self, event):
        #print 'menu'
        self.contextMenu.exec_(event.globalPos())
        event.accept()
        
    def enterEvent(self, event):
        self.highlightLabel.show()
        event.accept()
    
    def leaveEvent(self, event):
        self.highlightLabel.hide()
        event.accept()
        
    def getRect(self):
        """Return the rectangle describing the Zone geometry."""
        return (self.getPosY(), self.getPosX(), self.size().height(), self.size().width())
    
    def setPosition(self, x, y):
        """Sets the relative position within the level that contains the Zone."""
        self.position = (x,y)
        return None
    
    
    def getPosition(self):
        """Returns the relative position within the level that contains the Zone."""
        return self.position
    
    def getPosX(self):
        """Returns X Coord of the Zone."""
        return self.position[0]
    def getPosY(self):
        """Returns Y Coord of the Zone."""
        return self.position[1]
    
    def getDevices(self):
        """Gets the device widgets contained in the zone."""
        return self.__zoneDevices
    
    def addDevice(self, dev):
        """Adds a device widget to the Zone. Returns True if Successful.
    
        Prints an error if dev is not a HADevice.Device object.
        """
        if isinstance(dev, Device):
            self.interiorLayout.addWidget(dev, *dev.getRect())
            self.__zoneDevices.append(dev)
            return True
        else:
                print 'Zone <%s> Error: %s is not a Device'%(self.__name__,str(dev))
                return False
    
    def removeDevice(self, dev):
        """Removes and returns a device (Widget) from the Zone."""
        if dev in self.__zoneDevices:
            self.interiorLayout.removeWidget(dev)
            return self.__zoneDevices.remove(dev)
        else:
            print 'Zone Warning: The device %s was not in the Zone.'%dev
        return None
    
    def getNumberDevices(self):
        """Returns the number of devices contained within the Zone."""
        return len(self.__zoneDevices)
    
    def getNumberActive(self):
        active = 0
        for device in self.__zoneDevices:
            if device.isOn():
                active += 1
        return active
    
    def getName(self):
        """Returns the name of the Zone."""
        return self.__name__
    
    def showAddDeviceDialog(self):
        addDialog = dialogs.AddDeviceDialog(HAIS.DB_MGR)
        addDialog.exec_()
        return None
    
    def showRemoveDeviceDialog(self):
        removeDialog = dialogs.RemoveDeviceDialog(HAIS.DB_MGR)
        removeDialog.exec_()
        return None
    def turnOffDevices(self):
        for dev in self.__zoneDevices:
                if not dev.isLocked():
                 dev.turnOff()
        return None
    def turnOnDevices(self):
        for dev in self.__zoneDevices:
                if not dev.isLocked():
                 dev.turnOn()
        return None
    def __updateToolTip(self):
        return None

class Level(QWidget):
    """Acts as a container for the Zone Class.""" 
    def __init__(self, name, levelID = 0, parent = None):
        QWidget.__init__(self, parent)
        self.__name__ = name
        self.__levelID = levelID
        self.__levelZones = []
        self.interiorLayout = QGridLayout()
        self.interiorLayout.setSpacing(0)
        self.setLayout(QGridLayout())
        self.layout().addLayout(self.interiorLayout,1,1)
        self.layout().setSpacing(0)
        for x in range(0,3):
            for y in range(0,3):
                if not x is 1 and not y is 1:
                    self.layout().addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding),x,y)
        self.setPalette(QPalette(QColor(120,120,120)))
    def addZone(self, zn):
        """Adds a zone to the Level.
                
        If zn is not a Zone prints an error message.
        """
        if isinstance(zn, Zone):
            self.interiorLayout.addWidget(zn, *zn.getRect())
            self.__levelZones.append(zn)
            return True
        return False
   
    def getZones(self):
        return self.__levelZones
    
    def getDevices(self):
        allDevices = []
        for rm in self._rooms.values():
                allDevices.extend(rm.getDevices())
                
        return allDevices
    def getName(self):
        """Returns the name of the Level"""
        return self.__name__
    
    def getLevelID(self):
        return self.levelID
        
