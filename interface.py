from classes import KeyCode
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, QtCore, QtGui
from overlay_lib import RgbaColor, RgbaGradient

comboStyles = """
    QComboBox {
        background-color: rgba(33, 33, 33, 255);
        color: rgba(196, 18, 112, 255);
        padding: 5px;
        padding-top: 2px;
        padding-bottom: 2px; 
        border: 3px solid rgba(33, 33, 33, 255);
        border-radius: 5px;
    }
    QComboBox::down-arrow {
        image: url(assets/dropdown.png);
        margin-right: 2px;
        width: 10px;
        height: 10px;
    }
    QComboBox::drop-down {
        background-color: rgba(33, 33, 33, 255);
        color: rgba(196, 18, 112, 255);
        padding: 5px;
        border-radius: 5px;
    }
    QComboBox QAbstractItemView {
        color: rgba(196, 18, 112, 255);
        selection-background-color: rgba(196, 18, 112, 255);
        selection-color: rgba(33, 33, 33, 255);
        outline: 0;
    }
"""

checkBoxStyles = """
    QCheckBox {
        color: white;
        font-size: 12px;
    }
    QCheckBox::indicator {
        width: 12px;
        height: 12px;
        border: 2px solid rgba(33, 33, 33, 255);
        border-radius: 3px;
        background: rgba(33, 33, 33, 255);
    }
    QCheckBox::indicator:checked {
        width: 12px;
        height: 12px;
        image: url('assets/checkmark.png');
    }
"""

sliderStyles = """
    QSlider::groove:horizontal { 
        background-color: rgba(33, 33, 33, 255); 
        height: 10px; border-radius: 5px; 
    } 
    QSlider::handle:horizontal { 
        background-color: rgba(196, 18, 112, 255); 
        width: 10px; 
        height: 10px; 
        border-radius: 5px; 
    }
"""

inputStyles = """
    background-color: rgba(33, 33, 33, 255); 
    color: rgba(196, 18, 112, 255); 
    padding: 1px; 
    border: 3px solid rgba(33, 33, 33, 255); 
    border-radius: 5px;
"""

buttonStyles = """
    QPushButton {
        background-color: rgba(33, 33, 33, 255); 
        color: rgba(196, 18, 112, 255); 
        font-size: 12px; 
        border: 2px solid rgba(33, 33, 33, 255); 
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: rgba(196, 18, 112, 255);
        color: rgba(33, 33, 33, 255);
    }
"""

class CustomColorDialog(QtWidgets.QColorDialog):
    def __init__(self, *args, **kwargs):
        super(CustomColorDialog, self).__init__(*args, **kwargs)
        self.setOption(QtWidgets.QColorDialog.ShowAlphaChannel, True)
        
    @staticmethod
    def getColor(initial=None, parent=None, title="", options=None, defaultColor=QtGui.QColor(255, 255, 255, 255)):
        dialog = CustomColorDialog(parent)
        dialog.setWindowTitle(title)
        if initial:
            dialog.setCurrentColor(initial)
        if options:
            dialog.setOptions(options)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            return dialog.currentColor()
        else:
            return defaultColor

class GuiWindow(QtWidgets.QMainWindow):
    
    BUILD_NUMBER = "Beta v1.0.0"
    BUILD_TIME = "22-06-2024 | 11:12PM"
    VALID_TARGET_SETTINGS = ["center_coords", "head_coords", "torso_coords", "legs_coords", "penis_coords"]
    KEYCODES = {0x02: 'rightclick', 0x05: 'sidebackbutton', 0x06: 'sideforwardbutton', 0x11: 'controlkey', 0x10: 'shiftkey', 0x12: 'altkey', 0x20: 'spacebar', 0x0D: 'enterkey', 0x1B: 'escapekey', 0x25: 'leftarrow', 0x26: 'uparrow', 0x27: 'rightarrow', 0x28: 'downarrow'}
    
    def __init__(self, pixelbot_instance, parent=None,):
        super(GuiWindow, self).__init__(parent)
        
        self.isShowing = True
        self.isDragging = False
        
        self.pixelbot_instance = pixelbot_instance
        
        self.setWindowTitle("PixelBot")
        self.setGeometry(0, 0, 860, 600)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:0, stop:0.85 rgba(21, 21, 21, 255), stop:1 rgba(35, 39, 41, 255));")
        
        self.fontlogo = QtGui.QFont("Consolas", 20)
        
        self.header = QtWidgets.QFrame(self)
        self.header.setGeometry(0, 0, 860, 50)
        self.header.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.creditsstuff = QtWidgets.QLabel("Made By Takkeshi | https://takkeshi.pages.dev | https://github.com/LUXTACO", self.header)
        self.creditsstuff.setGeometry(0, 0, 860, 25)
        self.creditsstuff.setAlignment(QtCore.Qt.AlignRight)
        self.creditsstuff.setStyleSheet("color: rgba(255, 255, 255, 100); font-size: 12px; margin: 5px; margin-bottom: 0px;")
        self.versionnumber = QtWidgets.QLabel(f"Build: {self.BUILD_NUMBER} | {self.BUILD_TIME}", self.header)
        self.versionnumber.setGeometry(0, 20, 860, 25)
        self.versionnumber.setAlignment(QtCore.Qt.AlignRight)
        self.versionnumber.setStyleSheet("color: rgba(255, 255, 255, 100); font-size: 12px; margin: 5px; margin-top: 0px;")
        
        self.sidepanel = QtWidgets.QFrame(self)
        self.sidepanel.setGeometry(0, 0, 200, 600)
        self.sidepanel.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.logo = QtWidgets.QLabel(self.sidepanel)
        self.logo.setGeometry(0, 0, 200, 100)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setText("碲")
        self.logo.setStyleSheet("color: white; font-size: 60px;")
        self.logo.setFont(self.fontlogo)
        self.logo2 = QtWidgets.QLabel(self.sidepanel)
        self.logo2.setGeometry(0, 60, 200, 50)
        self.logo2.setAlignment(QtCore.Qt.AlignCenter)
        self.logo2.setText("Tekkuria")
        self.logo2.setFont(self.fontlogo)
        self.logo2.setStyleSheet("color: white; font-size: 20px; border-bottom: 1px solid rgba(255, 255, 255, 50);")
        
        self.hue = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateColor)
        self.timer.start(1)
        
        self.aimbotbutton = QtWidgets.QPushButton("     Aimbot", self.sidepanel)
        self.aimbotbutton.setGeometry(0, 110, 200, 50)
        
        self.aimbotbutton.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white; font-size: 15px; text-align: left;")
        self.visualsbutton = QtWidgets.QPushButton("     Visuals", self.sidepanel)
        self.visualsbutton.setGeometry(0, 160, 200, 50)
        
        self.visualsbutton.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white; font-size: 15px; text-align: left;")
        self.miscbutton = QtWidgets.QPushButton("     Misc", self.sidepanel)
        
        self.miscbutton.setGeometry(0, 210, 200, 50)
        self.miscbutton.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white; font-size: 15px; text-align: left;")
        
        self.configbutton = QtWidgets.QPushButton("     Config", self.sidepanel)
        self.configbutton.setGeometry(0, 550, 200, 50)
        self.configbutton.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white; font-size: 15px; text-align: left;")
        
        self.maincontainer = QtWidgets.QFrame(self)
        self.maincontainer.setGeometry(200, 50, 660, 570)
        self.maincontainer.setStyleSheet("background-color: rgba(43, 43, 43, 255);")
        
        self.aimbotbutton.clicked.connect(self.loadAimbot)
        self.visualsbutton.clicked.connect(self.loadVisuals)
        self.miscbutton.clicked.connect(self.loadMisc)
        self.configbutton.clicked.connect(self.loadConfig)
        
        self.loadAimbot()
    
    def updateColor(self):
        color = QtGui.QColor.fromHsl(self.hue, 255, 127)
        self.logo.setStyleSheet(f"color: {color.name()}; font-size: 60px;")
        self.logo2.setStyleSheet(f"color: {color.name()}; font-size: 20px; border-bottom: 1px solid rgba(255, 255, 255, 50);")
        self.hue = (self.hue + 1) % 360
    
    def resetGui(self):
        
        for child in self.maincontainer.children():
            child.deleteLater()
        
        for button in self.sidepanel.children():
            button.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white; font-size: 15px; text-align: left; border: 0;")

        self.aimbotbutton.setStyleSheet(
            self.aimbotbutton.styleSheet() + "background-image: url('assets/aimbot.png'); background-repeat: no-repeat; background-position: left center; padding-left: 12px; background-origin: content;"
        )
        self.visualsbutton.setStyleSheet(
            self.visualsbutton.styleSheet() + "background-image: url('assets/visuals.png'); background-repeat: no-repeat; background-position: left center; padding-left: 12px; background-origin: content;"
        )
        self.miscbutton.setStyleSheet(
            self.miscbutton.styleSheet() + "background-image: url('assets/misc.png'); background-repeat: no-repeat; background-position: left center; padding-left: 12px; background-origin: content;"
        )
        self.configbutton.setStyleSheet(
            self.configbutton.styleSheet() + "background-image: url('assets/config.png'); background-repeat: no-repeat; background-position: left center; padding-left: 12px; background-origin: content;"
        )
    
    def loadAimbot(self):
        
        self.resetGui()
                
        self.aimbotbutton.setStyleSheet("""background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(176, 40, 113), stop:1 rgb(123, 19, 78)); 
                                        color: white; font-size: 15px; border: 0; text-align: left;""")
        self.aimbotbutton.setStyleSheet(
            self.aimbotbutton.styleSheet() + "background-image: url('assets/aimbot.png'); background-repeat: no-repeat; background-position: left center; padding-left: 12px; background-origin: content;"
        )
        
        Aimbot.loadMain(self)
        Aimbot.loadContent(self)
        
        for child in self.maincontainer.children():
            child.show()
    
    def loadVisuals(self):
            
        self.resetGui()
                
        self.visualsbutton.setStyleSheet("""background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(176, 40, 113), stop:1 rgb(123, 19, 78)); 
                                        color: white; font-size: 15px; border: 0; text-align: left;""")
        self.visualsbutton.setStyleSheet(
            self.visualsbutton.styleSheet() + "background-image: url('assets/visuals.png'); background-repeat: no-repeat; background-position: left center; padding-left: 12px; background-origin: content;"
        )        
        
        Visuals.loadMain(self)
        Visuals.loadContent(self)
        
        for child in self.maincontainer.children():
            child.show()
    
    def loadMisc(self):
            
        self.resetGui()
                
        self.miscbutton.setStyleSheet("""background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(176, 40, 113), stop:1 rgb(123, 19, 78)); 
                                        color: white; font-size: 15px; border: 0; text-align: left;""")
        self.miscbutton.setStyleSheet(
            self.miscbutton.styleSheet() + "background-image: url('assets/misc.png'); background-repeat: no-repeat; background-position: left center; padding-left: 12px; background-origin: content;"
        )
        
        Misc.loadMain(self)
        Misc.loadContent(self)
        
        for child in self.maincontainer.children():
            child.show()
    
    def loadConfig(self):
        
        self.resetGui()
                
        self.configbutton.setStyleSheet("""background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(176, 40, 113), stop:1 rgb(123, 19, 78)); 
                                        color: white; font-size: 15px; border: 0; text-align: left;""")
        self.configbutton.setStyleSheet(
            self.configbutton.styleSheet() + "background-image: url('assets/config.png'); background-repeat: no-repeat; background-position: left center; padding-left: 12px; background-origin: content;"
        )
        
        ConfigTab.loadMain(self)
        ConfigTab.loadContent(self)
        
        for child in self.maincontainer.children():
            child.show()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Insert and self.isShowing:
            self.setWindowOpacity(0)
        elif event.key() == QtCore.Qt.Key_Insert and not self.isShowing:
            self.setWindowOpacity(1)
            
        self.isShowing = not self.isShowing
    
    def mousePressEvent(self, event):
        if event.pos().y() <= self.header.height():
            self.oldPos = event.globalPos()
            self.isDragging = True
        else:
            self.isDragging = False

    def mouseMoveEvent(self, event):
        if self.isDragging:
            delta = event.globalPos() - self.oldPos
            self.window().move(self.window().pos() + delta)
            self.oldPos = event.globalPos()
    
##############################################
    
    def smoothingsliderChange(self, value):
        try:
            float_value = value / 1000
            self.smoothinginput.setText(str(float_value))
            self.pixelbot_instance.config.smoothing = float_value
        except:
            pass
    
    def smoothinginputChange(self):
        try:
            value = float(self.smoothinginput.text())
            
            if value > 5:
                value = 5
            elif value < 0.1:
                value = 0.1
            
            self.smoothingslider.setValue(int(value * 1000))
            self.pixelbot_instance.config.smoothing = value
        except:
            pass
    
    def similaritysliderChange(self, value):
        try:
            self.similarityinput.setText(str(value))
            self.pixelbot_instance.updateColor(similarity=value)
        except:
            pass
    
    def similarityinputChange(self):
        try:
            value = int(self.similarityinput.text())
            
            if value > 255:
                value = 255
            elif value < 1:
                value = 1
            
            self.similarityslider.setValue(int(value))
            self.pixelbot_instance.updateColor(similarity=value)
        except:
            pass
        
    def distancesliderChange(self, value):
        try:
            self.distanceinput.setText(str(value))
            self.pixelbot_instance.config.mindistance = value
        except:
            pass
    
    def distanceinputChange(self):
        try:
            value = int(self.distanceinput.text())
            
            if value > 500:
                value = 500
            elif value < 1:
                value = 1
            
            self.distanceslider.setValue(value)
            self.pixelbot_instance.config.mindistance = value
        except Exception as e:
            print(e)
    
    def targetcolorChange(self):
        color = QtWidgets.QColorDialog.getColor()
        self.targetcolorcube.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.updateColor(targetcolor=[color.red(), color.green(), color.blue()])
        
    def fovsliderChange(self, value):
        try:
            self.fovinput.setText(str(value))
            self.pixelbot_instance.updateFOV(value)
        except:
            pass
    
    def fovinputChange(self):
        try: 
            value = int(self.fovinput.text())
            
            if value > 420:
                value = 420
            
            self.fovslider.setValue(value)
            self.pixelbot_instance.updateFOV(value)
        except:
            pass
          
    def targetboneChange(self):
        self.pixelbot_instance.config.targetbone = self.VALID_TARGET_SETTINGS[self.targetbonecombo.currentIndex()]
        
    def holdkeyChange(self):
        keyname = self.holdkeycombo.currentText()
        self.pixelbot_instance.config.holdkey = getattr(KeyCode, keyname)
    
    def togglekeyChange(self):
        keyname = self.togglekeycombo.currentText()
        self.pixelbot_instance.config.togglekey = getattr(KeyCode, keyname)
    
    def autoshootChange(self):
        self.pixelbot_instance.config.autoshoot = self.enableautoshoot.isChecked()
        
    def boxoutlinecolorChange(self):
        color = QtWidgets.QColorDialog.getColor()
        self.boxoutlinecolorcube.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.boxsettings.outlinecolor = RgbaColor(color.red(), color.green(), color.blue(), 255)
    
    def drawboxesChange(self):
        self.pixelbot_instance.config.drawbox = self.enabledrawboxes.isChecked()
    
    def drawboneChange(self):
        self.pixelbot_instance.config.drawbone = self.enabledrawbone.isChecked()
    
    def drawlinesChange(self):
        self.pixelbot_instance.config.drawlines = self.enabledrawlines.isChecked()
        
    def areainputChange(self):
        try:
            value = int(self.areainput.text())
            
            if value > 500:
                value = 500
            elif value < 1:
                value = 1
            
            self.areaslider.setValue(value)
            self.pixelbot_instance.config.minarea = value
        except:
            pass
    
    def areasliderChange(self, value):
        try:
            self.areainput.setText(str(value))
            self.pixelbot_instance.config.minarea = value
        except:
            pass
        
    def boneoutlinecolorChange(self):
        color = QtWidgets.QColorDialog.getColor()
        self.boneoutlinecolorcube.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.bonesettings.outlinecolor = RgbaColor(color.red(), color.green(), color.blue(), 255)

    def linescolorChange(self):
        color = QtWidgets.QColorDialog.getColor()
        self.linescolorcube.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.linescolor = RgbaColor(color.red(), color.green(), color.blue(), 255)
    
    def drawfovChange(self):
        self.pixelbot_instance.config.drawfov = self.enabledrawfov.isChecked()
    
    def fovoutlinecolorChange(self):
        color = CustomColorDialog.getColor()
        self.fovoutlinecolorcube.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.fovsettings.outlinecolor = RgbaColor(color.red(), color.green(), color.blue(), 255)
    
    def fovfillcolorChange1(self):
        color = CustomColorDialog.getColor()
        self.fovfillcolorcube1.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.fovsettings.fillcolor.from_rgba = RgbaColor(color.red(), color.green(), color.blue(), color.alpha())
        
    def fovfillcolorChange2(self):
        color = CustomColorDialog.getColor()
        self.fovfillcolorcube2.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba = RgbaColor(color.red(), color.green(), color.blue(), color.alpha())
    
    def boxfillcolorChange1(self):
        color = CustomColorDialog.getColor()
        self.boxfillcolorcube1.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.boxsettings.fillcolor.from_rgba = RgbaColor(color.red(), color.green(), color.blue(), color.alpha())
    
    def boxfillcolorChange2(self):
        color = CustomColorDialog.getColor()
        self.boxfillcolorcube2.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.boxsettings.fillcolor.to_rgba = RgbaColor(color.red(), color.green(), color.blue(), color.alpha()) 
    
    def fillboxChange(self):
        self.pixelbot_instance.config.boxsettings.fill = self.enablefillbox.isChecked()
    
    def fillfovChange(self):
        self.pixelbot_instance.config.fovsettings.fill = self.enablefillfov.isChecked()
    
    def fillboneChange(self):
        self.pixelbot_instance.config.bonesettings.fill = self.enablefillbone.isChecked()
    
    def bonefillcolorChange1(self):
        color = CustomColorDialog.getColor()
        self.bonefillcolorcube1.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.bonesettings.fillcolor.from_rgba = RgbaColor(color.red(), color.green(), color.blue(), color.alpha())
    
    def bonefillcolorChange2(self):
        color = CustomColorDialog.getColor()
        self.bonefillcolorcube2.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.pixelbot_instance.config.bonesettings.fillcolor.to_rgba = RgbaColor(color.red(), color.green(), color.blue(), color.alpha())
    
    def loadConfigFile(self):
        configname = self.selectconfigcombo.currentText()
        
        if not configname:
            return
        
        self.pixelbot_instance.loadConfig(configname) 
        self.loadConfig()
    
    def saveConfigFile(self):
        configname = self.selectconfigcombo.currentText()

        if not configname:
            return
        
        if not configname.endswith(".json"):
            configname = f"{configname}.json"
        
        self.pixelbot_instance.saveConfig(configname)
        self.loadConfig()
    
    def deleteConfigFile(self):
        configname = self.selectconfigcombo.currentText()
        
        if not configname:
            return
        
        self.pixelbot_instance.deleteConfig(configname)
        self.loadConfig()
        
    def createConfigFile(self):
        configname = self.selectconfigcombo.currentText()
        
        if not configname:
            return
        
        if not configname.endswith(".json"):
            configname = f"{configname}.json"
        
        self.pixelbot_instance.createConfig(configname)
        self.loadConfig()
    
    def changeinputHeadOffset(self):
        try:
            value = float(self.headoffsetinput.text())
            self.pixelbot_instance.config.headoffset = value
        except:
            pass
    
    def changeinputTorsoOffset(self):
        try:
            value = float(self.torsooffsetinput.text())
            self.pixelbot_instance.config.torsooffset = value
        except:
            pass
    
    def changeinputLegsOffset(self):
        try:
            value = float(self.legoffsetinput.text())
            self.pixelbot_instance.config.legsoffset = value
        except:
            pass    
    
    def changeinputPenisOffset(self):
        try:
            value = self.penisoffsetinput.text()
            self.pixelbot_instance.config.penisoffset = value
        except:
            pass
        
    def triggerfovinputChange(self):
        try:
            value = int(self.triggerfovinput.text())
            
            if value > 420:
                value = 420
            elif value < 1:
                value = 1
            
            self.triggerfovslider.setValue(value)
            self.pixelbot_instance.config.triggerfov = value
        except:
            pass
        
    def triggerfovsliderChange(self, value):
        try:
            self.triggerfovinput.setText(str(value))
            self.pixelbot_instance.config.triggerfov = value
        except:
            pass
        
    def changeinputtargetfps(self):
        try:
            value = int(self.targetfpsinput.text())
            
            if value > 240:
                value = 240
            elif value < 1:
                value = 1
                
            self.pixelbot_instance.updateFPS(value)
        except:
            pass
        
##############################################

class Aimbot: 
    
    def loadMain(self):
        self.panelAim = QtWidgets.QFrame(self.maincontainer)
        self.panelAim.setGeometry(0, 0, 660, 275)
        self.panelAim.setStyleSheet("background-color: rgba(27, 27, 27, 255); margin: 10px; margin-bottom: 5px;")
        self.panelLocal = QtWidgets.QLabel("Aimbot Settings", self.panelAim)
        self.panelLocal.setGeometry(0, 0, 660, 40)
        self.panelLocal.setAlignment(QtCore.Qt.AlignCenter)
        self.panelLocal.setStyleSheet("color: white; font-size: 15px; border-bottom: 1px solid rgba(255, 255, 255, 50);")
        
        self.panelDetec = QtWidgets.QFrame(self.maincontainer)
        self.panelDetec.setGeometry(0, 275, 660, 275)
        self.panelDetec.setStyleSheet("background-color: rgba(27, 27, 27, 255); margin: 10px; margin-top: 5px;")
        self.panelLocal = QtWidgets.QLabel("Detection Settings", self.panelDetec)
        self.panelLocal.setGeometry(0, 0, 660, 40)
        self.panelLocal.setAlignment(QtCore.Qt.AlignCenter)
        self.panelLocal.setStyleSheet("color: white; font-size: 15px; border-bottom: 1px solid rgba(255, 255, 255, 50);")
    
    def loadContent(self):
        Aimbot.loadContentAim(self)
        Aimbot.loadContentDetec(self)
    
    def loadContentAim(self):
        self.leftcontainer = QtWidgets.QFrame(self.panelAim)
        self.leftcontainer.setGeometry(0, 25, 340, 250)
        self.leftcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.autoshootcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.autoshootcontainer.setGeometry(2, 0, 340, 40)
        self.autoshootcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enableautoshoot = QtWidgets.QCheckBox("Enable triggerbot", self.autoshootcontainer)
        self.enableautoshoot.setGeometry(0, 0, 340, 40)
        self.enableautoshoot.setStyleSheet(checkBoxStyles)
        self.enableautoshoot.setChecked(self.pixelbot_instance.config.autoshoot)
        self.enableautoshoot.stateChanged.connect(self.autoshootChange)
        
        self.holdkeycontainer = QtWidgets.QFrame(self.leftcontainer)
        self.holdkeycontainer.setGeometry(0, 30, 340, 40)
        self.holdkeycontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.holdkeylabel = QtWidgets.QLabel("Hold key", self.holdkeycontainer)
        self.holdkeylabel.setGeometry(0, 0, 100, 40)
        self.holdkeylabel.setStyleSheet("color: white; font-size: 12px;")
        self.holdkeycombo = QtWidgets.QComboBox(self.holdkeycontainer)
        self.holdkeycombo.setGeometry(100, 0, 230, 40)
        self.holdkeycombo.setStyleSheet(comboStyles)
        
        self.togglekeycontainer = QtWidgets.QFrame(self.leftcontainer)
        self.togglekeycontainer.setGeometry(0, 65, 340, 40)
        self.togglekeycontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.togglekeylabel = QtWidgets.QLabel("Toggle key", self.togglekeycontainer)
        self.togglekeylabel.setGeometry(0, 0, 100, 40)
        self.togglekeylabel.setStyleSheet("color: white; font-size: 12px;")
        self.togglekeycombo = QtWidgets.QComboBox(self.togglekeycontainer)
        self.togglekeycombo.setGeometry(100, 0, 230, 40)
        self.togglekeycombo.setStyleSheet(comboStyles)
        
        self.targetbonecontainer = QtWidgets.QFrame(self.leftcontainer)
        self.targetbonecontainer.setGeometry(0, 100, 340, 40)
        self.targetbonecontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.targetbonelabel = QtWidgets.QLabel("Target bone", self.targetbonecontainer)
        self.targetbonelabel.setGeometry(0, 0, 120, 40)
        self.targetbonelabel.setStyleSheet("color: white; font-size: 12px;")
        self.targetbonecombo = QtWidgets.QComboBox(self.targetbonecontainer)
        self.targetbonecombo.setGeometry(100, 0, 230, 40)
        self.targetbonecombo.setStyleSheet(comboStyles)
        
        self.rightcontainer = QtWidgets.QFrame(self.panelAim)
        self.rightcontainer.setGeometry(320, 25, 340, 250)
        self.rightcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.smoothingcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.smoothingcontainer.setGeometry(2, 0, 340, 60)
        self.smoothingcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.smoothinglabel = QtWidgets.QLabel("Smoothing", self.smoothingcontainer)
        self.smoothinglabel.setGeometry(0, 0, 100, 40)
        self.smoothinglabel.setStyleSheet("color: white; font-size: 12px;")
        self.smoothinginput = QtWidgets.QLineEdit(self.smoothingcontainer)
        self.smoothinginput.setGeometry(265, 4, 60, 35)
        self.smoothinginput.setStyleSheet(inputStyles)
        self.smoothingslider = QtWidgets.QSlider(self.smoothingcontainer)
        self.smoothingslider.setGeometry(0, 30, 330, 20)
        self.smoothingslider.setOrientation(QtCore.Qt.Horizontal)
        self.smoothingslider.setStyleSheet(sliderStyles)
        self.smoothingslider.setMinimum(100)
        self.smoothingslider.setMaximum(5000)
        self.smoothingslider.setValue(int(self.pixelbot_instance.config.smoothing * 1000))
        self.smoothingslider.valueChanged.connect(self.smoothingsliderChange)
        self.smoothinginput.setText(str(self.pixelbot_instance.config.smoothing))
        self.smoothinginput.textChanged.connect(self.smoothinginputChange)
        
        self.fovcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.fovcontainer.setGeometry(2, 50, 340, 60)
        self.fovcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.fovlabel = QtWidgets.QLabel("Fov size", self.fovcontainer)
        self.fovlabel.setGeometry(0, 0, 100, 40)
        self.fovlabel.setStyleSheet("color: white; font-size: 12px;")
        self.fovinput = QtWidgets.QLineEdit(self.fovcontainer)
        self.fovinput.setGeometry(265, 4, 60, 35)
        self.fovinput.setStyleSheet(inputStyles)
        self.fovslider = QtWidgets.QSlider(self.fovcontainer)
        self.fovslider.setGeometry(0, 30, 330, 20)
        self.fovslider.setOrientation(QtCore.Qt.Horizontal)
        self.fovslider.setStyleSheet(sliderStyles)
        self.fovslider.setMinimum(1)
        self.fovslider.setMaximum(420)
        self.fovslider.setValue(self.pixelbot_instance.config.fovsize)
        self.fovinput.setText(str(self.pixelbot_instance.config.fovsize))
        self.fovinput.textChanged.connect(self.fovinputChange)
        self.fovslider.valueChanged.connect(self.fovsliderChange)
        
        self.triggerfovcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.triggerfovcontainer.setGeometry(2, 100, 340, 60)
        self.triggerfovcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.triggerfovlabel = QtWidgets.QLabel("Triggerbot fov size", self.triggerfovcontainer)
        self.triggerfovlabel.setGeometry(0, 0, 200, 40)
        self.triggerfovlabel.setStyleSheet("color: white; font-size: 12px;")
        self.triggerfovinput = QtWidgets.QLineEdit(self.triggerfovcontainer)
        self.triggerfovinput.setGeometry(265, 4, 60, 35)
        self.triggerfovinput.setStyleSheet(inputStyles)
        self.triggerfovslider = QtWidgets.QSlider(self.triggerfovcontainer)
        self.triggerfovslider.setGeometry(0, 30, 330, 20)
        self.triggerfovslider.setOrientation(QtCore.Qt.Horizontal)
        self.triggerfovslider.setStyleSheet(sliderStyles)
        self.triggerfovslider.setMinimum(1)
        self.triggerfovslider.setMaximum(420)
        self.triggerfovslider.setValue(self.pixelbot_instance.config.triggerfov)
        self.triggerfovinput.setText(str(self.pixelbot_instance.config.triggerfov))
        self.triggerfovinput.textChanged.connect(self.triggerfovinputChange)
        self.triggerfovslider.valueChanged.connect(self.triggerfovsliderChange)
        
        for item in KeyCode.__dict__: 
            if not item.startswith("__"):
                self.togglekeycombo.addItem(item)
                self.holdkeycombo.addItem(item)
        
        self.holdkeycombo.setCurrentText(f"{self.KEYCODES[self.pixelbot_instance.config.holdkey]}")
        self.togglekeycombo.setCurrentText(f"{self.KEYCODES[self.pixelbot_instance.config.togglekey]}")
        self.togglekeycombo.currentIndexChanged.connect(self.togglekeyChange)
        self.holdkeycombo.currentIndexChanged.connect(self.holdkeyChange)
                
        for item in self.VALID_TARGET_SETTINGS:
            self.targetbonecombo.addItem(item)
        
        self.targetbonecombo.setCurrentText(self.pixelbot_instance.config.targetbone)
        self.targetbonecombo.currentIndexChanged.connect(self.targetboneChange)
    
    def loadContentDetec(self): 
        self.leftcontainer = QtWidgets.QFrame(self.panelDetec)
        self.leftcontainer.setGeometry(0, 25, 340, 250)
        self.leftcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.distancecontainer = QtWidgets.QFrame(self.leftcontainer)
        self.distancecontainer.setGeometry(2, 0, 340, 60)
        self.distancecontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.distancelabel = QtWidgets.QLabel("Min distance", self.distancecontainer)
        self.distancelabel.setGeometry(0, 0, 100, 40)
        self.distancelabel.setStyleSheet("color: white; font-size: 12px;")
        self.distanceinput = QtWidgets.QLineEdit(self.distancecontainer)
        self.distanceinput.setGeometry(265, 4, 60, 35)
        self.distanceinput.setStyleSheet(inputStyles)
        self.distanceslider = QtWidgets.QSlider(self.distancecontainer)
        self.distanceslider.setGeometry(0, 30, 330, 20)
        self.distanceslider.setOrientation(QtCore.Qt.Horizontal)
        self.distanceslider.setStyleSheet(sliderStyles)
        self.distanceslider.setMinimum(1)
        self.distanceslider.setMaximum(500)
        self.distanceslider.setValue(self.pixelbot_instance.config.mindistance)
        self.distanceinput.setText(str(self.pixelbot_instance.config.mindistance))
        self.distanceinput.textChanged.connect(self.distanceinputChange)
        self.distanceslider.valueChanged.connect(self.distancesliderChange)
        
        self.areacontainer = QtWidgets.QFrame(self.leftcontainer)
        self.areacontainer.setGeometry(2, 50, 340, 60)
        self.areacontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.arealabel = QtWidgets.QLabel("Min area", self.areacontainer)
        self.arealabel.setGeometry(0, 0, 100, 40)
        self.arealabel.setStyleSheet("color: white; font-size: 12px;")
        self.areainput = QtWidgets.QLineEdit(self.areacontainer)
        self.areainput.setGeometry(265, 4, 60, 35)
        self.areainput.setStyleSheet(inputStyles)
        self.areaslider = QtWidgets.QSlider(self.areacontainer)
        self.areaslider.setGeometry(0, 30, 330, 20)
        self.areaslider.setOrientation(QtCore.Qt.Horizontal)
        self.areaslider.setStyleSheet(sliderStyles)
        self.areaslider.setMinimum(1)
        self.areaslider.setMaximum(500)
        self.areaslider.setValue(self.pixelbot_instance.config.minarea)
        self.areainput.setText(str(self.pixelbot_instance.config.minarea))
        self.areainput.textChanged.connect(self.areainputChange)
        self.areaslider.valueChanged.connect(self.areasliderChange)
        
        self.rightcontainer = QtWidgets.QFrame(self.panelDetec)
        self.rightcontainer.setGeometry(320, 25, 340, 250)
        self.rightcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.similaritycontainer = QtWidgets.QFrame(self.rightcontainer)
        self.similaritycontainer.setGeometry(2, 0, 340, 60)
        self.similaritycontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.similaritylabel = QtWidgets.QLabel("Similarity", self.similaritycontainer)
        self.similaritylabel.setGeometry(0, 0, 100, 40)
        self.similaritylabel.setStyleSheet("color: white; font-size: 12px;")
        self.similarityinput = QtWidgets.QLineEdit(self.similaritycontainer)
        self.similarityinput.setGeometry(265, 4, 60, 35)
        self.similarityinput.setStyleSheet(inputStyles)
        self.similarityslider = QtWidgets.QSlider(self.similaritycontainer)
        self.similarityslider.setGeometry(0, 30, 330, 20)
        self.similarityslider.setOrientation(QtCore.Qt.Horizontal)
        self.similarityslider.setStyleSheet(sliderStyles)
        self.similarityslider.setMinimum(1)
        self.similarityslider.setMaximum(255)
        self.similarityslider.setValue(self.pixelbot_instance.config.similarity)
        self.similarityinput.setText(str(self.pixelbot_instance.config.similarity))
        self.similarityinput.textChanged.connect(self.similarityinputChange)
        self.similarityslider.valueChanged.connect(self.similaritysliderChange)
        
        self.targetcolorcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.targetcolorcontainer.setGeometry(2, 50, 340, 80)
        self.targetcolorcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.targetcolorlabel = QtWidgets.QLabel("Target color", self.targetcolorcontainer)
        self.targetcolorlabel.setGeometry(0, 0, 100, 40)
        self.targetcolorlabel.setStyleSheet("color: white; font-size: 12px;")
        self.targetcolorcube = QtWidgets.QFrame(self.targetcolorcontainer)
        self.targetcolorcube.setGeometry(265, 4, 60, 35)
        self.targetcolorcube.setStyleSheet(f"background-color: rgb({self.pixelbot_instance.config.targetcolor[0]}, {self.pixelbot_instance.config.targetcolor[1]}, {self.pixelbot_instance.config.targetcolor[2]}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.targetcolorchangebutton = QtWidgets.QPushButton("Change Color", self.targetcolorcontainer)
        self.targetcolorchangebutton.setGeometry(0, 30, 330, 45)
        self.targetcolorchangebutton.setStyleSheet(buttonStyles)
        self.targetcolorchangebutton.clicked.connect(self.targetcolorChange)
                
class Visuals:
    
    def loadMain(self):
        self.panelVisuals = QtWidgets.QFrame(self.maincontainer)
        self.panelVisuals.setGeometry(0, 0, 660, 545)
        self.panelVisuals.setStyleSheet("background-color: rgba(27, 27, 27, 255); margin: 10px; margin-bottom: 5px;")
        self.panelTitle = QtWidgets.QLabel("Visual Settings", self.panelVisuals)
        self.panelTitle.setGeometry(0, 0, 660, 40)
        self.panelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.panelTitle.setStyleSheet("color: white; font-size: 15px; border-bottom: 1px solid rgba(255, 255, 255, 50);")
    
    def loadContent(self):
        Visuals.loadContentVisuals(self)
        
    def loadContentVisuals(self):
        self.leftcontainer = QtWidgets.QFrame(self.panelVisuals)
        self.leftcontainer.setGeometry(0, 25, 340, 540)
        self.leftcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.drawboxescontainer = QtWidgets.QFrame(self.leftcontainer)
        self.drawboxescontainer.setGeometry(2, 0, 340, 40)
        self.drawboxescontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enabledrawboxes = QtWidgets.QCheckBox("Draw boxes", self.drawboxescontainer)
        self.enabledrawboxes.setGeometry(0, 0, 340, 40)
        self.enabledrawboxes.setStyleSheet(checkBoxStyles)
        self.enabledrawboxes.setChecked(self.pixelbot_instance.config.drawbox)
        self.enabledrawboxes.stateChanged.connect(self.drawboxesChange)
        
        self.drawbonecontainer = QtWidgets.QFrame(self.leftcontainer)
        self.drawbonecontainer.setGeometry(100, 0, 340, 40)
        self.drawbonecontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enabledrawbone = QtWidgets.QCheckBox("Draw bones", self.drawbonecontainer)
        self.enabledrawbone.setGeometry(0, 0, 340, 40)
        self.enabledrawbone.setStyleSheet(checkBoxStyles)
        self.enabledrawbone.setChecked(self.pixelbot_instance.config.drawbox)
        self.enabledrawbone.stateChanged.connect(self.drawboneChange)
        
        self.drawlinescontainer = QtWidgets.QFrame(self.leftcontainer)
        self.drawlinescontainer.setGeometry(210, 0, 340, 40)
        self.drawlinescontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enabledrawlines = QtWidgets.QCheckBox("Draw lines", self.drawlinescontainer)
        self.enabledrawlines.setGeometry(0, 0, 340, 40)
        self.enabledrawlines.setStyleSheet(checkBoxStyles)
        self.enabledrawlines.setChecked(self.pixelbot_instance.config.drawlines)
        self.enabledrawlines.stateChanged.connect(self.drawlinesChange)
        
        self.boxoutlinecolorcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.boxoutlinecolorcontainer.setGeometry(7, 30, 340, 80)
        self.boxoutlinecolorcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.boxoutlinecolorlabel = QtWidgets.QLabel("Outline color", self.boxoutlinecolorcontainer)
        self.boxoutlinecolorlabel.setGeometry(0, 0, 200, 40)
        self.boxoutlinecolorlabel.setStyleSheet("color: white; font-size: 12px;")
        self.boxoutlinecolorcube = QtWidgets.QFrame(self.boxoutlinecolorcontainer)
        self.boxoutlinecolorcube.setGeometry(265, 4, 60, 35)
        self.boxoutlinecolorcube.setStyleSheet(f"background-color: rgb({self.pixelbot_instance.config.boxsettings.outlinecolor.r}, {self.pixelbot_instance.config.boxsettings.outlinecolor.g}, {self.pixelbot_instance.config.boxsettings.outlinecolor.b}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.boxoutlinecolorchangebutton = QtWidgets.QPushButton("Change Color", self.boxoutlinecolorcontainer)
        self.boxoutlinecolorchangebutton.setGeometry(0, 30, 330, 45)
        self.boxoutlinecolorchangebutton.setStyleSheet(buttonStyles)
        self.boxoutlinecolorchangebutton.clicked.connect(self.boxoutlinecolorChange)
        
        self.boneoutlinecolorcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.boneoutlinecolorcontainer.setGeometry(7, 95, 340, 80)
        self.boneoutlinecolorcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.boneoutlinecolorlabel = QtWidgets.QLabel("Bone color", self.boneoutlinecolorcontainer)
        self.boneoutlinecolorlabel.setGeometry(0, 0, 200, 40)
        self.boneoutlinecolorlabel.setStyleSheet("color: white; font-size: 12px;")
        self.boneoutlinecolorcube = QtWidgets.QFrame(self.boneoutlinecolorcontainer)
        self.boneoutlinecolorcube.setGeometry(265, 4, 60, 35)
        self.boneoutlinecolorcube.setStyleSheet(f"background-color: rgb({self.pixelbot_instance.config.bonesettings.outlinecolor.r}, {self.pixelbot_instance.config.bonesettings.outlinecolor.g}, {self.pixelbot_instance.config.bonesettings.outlinecolor.b}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.boneoutlinecolorchangebutton = QtWidgets.QPushButton("Change Color", self.boneoutlinecolorcontainer)
        self.boneoutlinecolorchangebutton.setGeometry(0, 30, 330, 45)
        self.boneoutlinecolorchangebutton.setStyleSheet(buttonStyles)
        self.boneoutlinecolorchangebutton.clicked.connect(self.boneoutlinecolorChange)
        
        self.linescolorcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.linescolorcontainer.setGeometry(7, 160, 340, 80)
        self.linescolorcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.linescolorlabel = QtWidgets.QLabel("Line color", self.linescolorcontainer)
        self.linescolorlabel.setGeometry(0, 0, 200, 40)
        self.linescolorlabel.setStyleSheet("color: white; font-size: 12px;")
        self.linescolorcube = QtWidgets.QFrame(self.linescolorcontainer)
        self.linescolorcube.setGeometry(265, 4, 60, 35)
        self.linescolorcube.setStyleSheet(f"background-color: rgb({self.pixelbot_instance.config.linescolor.r}, {self.pixelbot_instance.config.linescolor.g}, {self.pixelbot_instance.config.linescolor.b}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.linescolorchangebutton = QtWidgets.QPushButton("Change Color", self.linescolorcontainer)
        self.linescolorchangebutton.setGeometry(0, 30, 330, 45)
        self.linescolorchangebutton.setStyleSheet(buttonStyles)
        self.linescolorchangebutton.clicked.connect(self.linescolorChange)
        
        self.fovoutlinecolorcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.fovoutlinecolorcontainer.setGeometry(7, 230, 340, 80)
        self.fovoutlinecolorcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.fovoutlinecolorlabel = QtWidgets.QLabel("Fov color", self.fovoutlinecolorcontainer)
        self.fovoutlinecolorlabel.setGeometry(0, 0, 200, 40)
        self.fovoutlinecolorlabel.setStyleSheet("color: white; font-size: 12px;")
        self.fovoutlinecolorcube = QtWidgets.QFrame(self.fovoutlinecolorcontainer)
        self.fovoutlinecolorcube.setGeometry(265, 4, 60, 35)
        self.fovoutlinecolorcube.setStyleSheet(f"background-color: rgb({self.pixelbot_instance.config.boxsettings.outlinecolor.r}, {self.pixelbot_instance.config.boxsettings.outlinecolor.g}, {self.pixelbot_instance.config.boxsettings.outlinecolor.b}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.fovoutlinecolorchangebutton = QtWidgets.QPushButton("Change Color", self.fovoutlinecolorcontainer)
        self.fovoutlinecolorchangebutton.setGeometry(0, 30, 330, 45)
        self.fovoutlinecolorchangebutton.setStyleSheet(buttonStyles)
        self.fovoutlinecolorchangebutton.clicked.connect(self.fovoutlinecolorChange)
        
        self.rightcontainer = QtWidgets.QFrame(self.panelVisuals)
        self.rightcontainer.setGeometry(320, 25, 340, 540)
        self.rightcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.drawfovcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.drawfovcontainer.setGeometry(2, 0, 340, 40)
        self.drawfovcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enabledrawfov = QtWidgets.QCheckBox("Draw fov", self.drawfovcontainer)
        self.enabledrawfov.setGeometry(0, 0, 340, 40)
        self.enabledrawfov.setStyleSheet(checkBoxStyles)
        self.enabledrawfov.setChecked(self.pixelbot_instance.config.drawfov)
        self.enabledrawfov.stateChanged.connect(self.drawfovChange)
        
        self.fillboxcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.fillboxcontainer.setGeometry(90, 0, 340, 40)
        self.fillboxcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enablefillbox = QtWidgets.QCheckBox("Fill box", self.fillboxcontainer)
        self.enablefillbox.setGeometry(0, 0, 340, 40)
        self.enablefillbox.setStyleSheet(checkBoxStyles)
        self.enablefillbox.setChecked(self.pixelbot_instance.config.boxsettings.fill)
        self.enablefillbox.stateChanged.connect(self.fillboxChange)
        
        self.fillfovcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.fillfovcontainer.setGeometry(170, 0, 340, 40)
        self.fillfovcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enablefillfov = QtWidgets.QCheckBox("Fill fov", self.fillfovcontainer)
        self.enablefillfov.setGeometry(0, 0, 340, 40)
        self.enablefillfov.setStyleSheet(checkBoxStyles)
        self.enablefillfov.setChecked(self.pixelbot_instance.config.fovsettings.fill)
        self.enablefillfov.stateChanged.connect(self.fillfovChange)
        
        self.fillbonecontainer = QtWidgets.QFrame(self.rightcontainer)
        self.fillbonecontainer.setGeometry(240, 0, 340, 40)
        self.fillbonecontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.enablefillbone = QtWidgets.QCheckBox("Fill bone", self.fillbonecontainer)
        self.enablefillbone.setGeometry(0, 0, 340, 40)
        self.enablefillbone.setStyleSheet(checkBoxStyles)
        self.enablefillbone.setChecked(self.pixelbot_instance.config.bonesettings.fill)
        self.enablefillbone.stateChanged.connect(self.fillboneChange)
        
        self.boxfillcolorcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.boxfillcolorcontainer.setGeometry(7, 30, 340, 80)
        self.boxfillcolorcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.boxfillcolorlabel = QtWidgets.QLabel("Box fill gradient", self.boxfillcolorcontainer)
        self.boxfillcolorlabel.setGeometry(0, 0, 200, 40)
        self.boxfillcolorlabel.setStyleSheet("color: white; font-size: 12px;")
        self.boxfillcolorcube1 = QtWidgets.QFrame(self.boxfillcolorcontainer)
        self.boxfillcolorcube1.setGeometry(220, 4, 60, 35)
        self.boxfillcolorcube1.setStyleSheet(f"background-color: rgba({self.pixelbot_instance.config.boxsettings.fillcolor.from_rgba.r}, {self.pixelbot_instance.config.boxsettings.fillcolor.from_rgba.g}, {self.pixelbot_instance.config.boxsettings.fillcolor.from_rgba.b}, {self.pixelbot_instance.config.boxsettings.fillcolor.from_rgba.a}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.boxfillcolorcube2 = QtWidgets.QFrame(self.boxfillcolorcontainer)
        self.boxfillcolorcube2.setGeometry(265, 4, 60, 35)
        self.boxfillcolorcube2.setStyleSheet(f"background-color: rgba({self.pixelbot_instance.config.boxsettings.fillcolor.to_rgba.r}, {self.pixelbot_instance.config.boxsettings.fillcolor.to_rgba.g}, {self.pixelbot_instance.config.boxsettings.fillcolor.to_rgba.b}, {self.pixelbot_instance.config.boxsettings.fillcolor.to_rgba.a}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.boxfillcolorchangebutton1 = QtWidgets.QPushButton("Change First Color", self.boxfillcolorcontainer)
        self.boxfillcolorchangebutton1.setGeometry(0, 30, 170, 45)
        self.boxfillcolorchangebutton1.setStyleSheet(buttonStyles)
        self.boxfillcolorchangebutton1.clicked.connect(self.boxfillcolorChange1)
        self.boxfillcolorchangebutton2 = QtWidgets.QPushButton("Change Second Color", self.boxfillcolorcontainer)
        self.boxfillcolorchangebutton2.setGeometry(155, 30, 170, 45)
        self.boxfillcolorchangebutton2.setStyleSheet(buttonStyles)
        self.boxfillcolorchangebutton2.clicked.connect(self.boxfillcolorChange2)
        
        self.bonefillcolorcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.bonefillcolorcontainer.setGeometry(7, 95, 340, 80)
        self.bonefillcolorcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.bonefillcolorlabel = QtWidgets.QLabel("Bone fill gradient", self.bonefillcolorcontainer)
        self.bonefillcolorlabel.setGeometry(0, 0, 200, 40)
        self.bonefillcolorlabel.setStyleSheet("color: white; font-size: 12px;")
        self.bonefillcolorcube1 = QtWidgets.QFrame(self.bonefillcolorcontainer)
        self.bonefillcolorcube1.setGeometry(220, 4, 60, 35)
        self.bonefillcolorcube1.setStyleSheet(f"background-color: rgba({self.pixelbot_instance.config.bonesettings.fillcolor.from_rgba.r}, {self.pixelbot_instance.config.bonesettings.fillcolor.from_rgba.g}, {self.pixelbot_instance.config.bonesettings.fillcolor.from_rgba.b}, {self.pixelbot_instance.config.bonesettings.fillcolor.from_rgba.a}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.bonefillcolorcube2 = QtWidgets.QFrame(self.bonefillcolorcontainer)
        self.bonefillcolorcube2.setGeometry(265, 4, 60, 35)
        self.bonefillcolorcube2.setStyleSheet(f"background-color: rgba({self.pixelbot_instance.config.bonesettings.fillcolor.to_rgba.r}, {self.pixelbot_instance.config.bonesettings.fillcolor.to_rgba.g}, {self.pixelbot_instance.config.bonesettings.fillcolor.to_rgba.b}, {self.pixelbot_instance.config.bonesettings.fillcolor.to_rgba.a}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.bonefillcolorchangebutton1 = QtWidgets.QPushButton("Change First Color", self.bonefillcolorcontainer)
        self.bonefillcolorchangebutton1.setGeometry(0, 30, 170, 45)
        self.bonefillcolorchangebutton1.setStyleSheet(buttonStyles)
        self.bonefillcolorchangebutton1.clicked.connect(self.bonefillcolorChange1)
        self.bonefillcolorchangebutton2 = QtWidgets.QPushButton("Change Second Color", self.bonefillcolorcontainer)
        self.bonefillcolorchangebutton2.setGeometry(155, 30, 170, 45)
        self.bonefillcolorchangebutton2.setStyleSheet(buttonStyles)
        self.bonefillcolorchangebutton2.clicked.connect(self.bonefillcolorChange2)
        
        self.fovfillcolorcontainer = QtWidgets.QFrame(self.rightcontainer)
        self.fovfillcolorcontainer.setGeometry(7, 230, 340, 80)
        self.fovfillcolorcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.fovfillcolorlabel = QtWidgets.QLabel("Fov fill gradient", self.fovfillcolorcontainer)
        self.fovfillcolorlabel.setGeometry(0, 0, 200, 40)
        self.fovfillcolorlabel.setStyleSheet("color: white; font-size: 12px;")
        self.fovfillcolorcube1 = QtWidgets.QFrame(self.fovfillcolorcontainer)
        self.fovfillcolorcube1.setGeometry(220, 4, 60, 35)
        self.fovfillcolorcube1.setStyleSheet(f"background-color: rgba({self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba.r}, {self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba.g}, {self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba.b}, {self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba.a}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.fovfillcolorcube2 = QtWidgets.QFrame(self.fovfillcolorcontainer)
        self.fovfillcolorcube2.setGeometry(265, 4, 60, 35)
        self.fovfillcolorcube2.setStyleSheet(f"background-color: rgba({self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba.r}, {self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba.g}, {self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba.b}, {self.pixelbot_instance.config.fovsettings.fillcolor.to_rgba.a}); border: 2px solid rgba(33, 33, 33, 255); border-radius: 5px;")
        self.fovfillcolorchangebutton1 = QtWidgets.QPushButton("Change First Color", self.fovfillcolorcontainer)
        self.fovfillcolorchangebutton1.setGeometry(0, 30, 170, 45)
        self.fovfillcolorchangebutton1.setStyleSheet(buttonStyles)
        self.fovfillcolorchangebutton1.clicked.connect(self.fovfillcolorChange1)
        self.fovfillcolorchangebutton2 = QtWidgets.QPushButton("Change Second Color", self.fovfillcolorcontainer)
        self.fovfillcolorchangebutton2.setGeometry(155, 30, 170, 45)
        self.fovfillcolorchangebutton2.setStyleSheet(buttonStyles)
        self.fovfillcolorchangebutton2.clicked.connect(self.fovfillcolorChange2)
           
class Misc:
    
    def loadMain(self):
        self.panelMisc = QtWidgets.QFrame(self.maincontainer)
        self.panelMisc.setGeometry(0, 0, 660, 545)
        self.panelMisc.setStyleSheet("background-color: rgba(27, 27, 27, 255); margin: 10px; margin-bottom: 5px;")
        self.panelTitle = QtWidgets.QLabel("Misc Settings", self.panelMisc)
        self.panelTitle.setGeometry(0, 0, 660, 40)
        self.panelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.panelTitle.setStyleSheet("color: white; font-size: 15px; border-bottom: 1px solid rgba(255, 255, 255, 50);")
    
    def loadContent(self):
        Misc.loadContentMisc(self)
        
    def loadContentMisc(self):
        self.leftcontainer = QtWidgets.QFrame(self.panelMisc)
        self.leftcontainer.setGeometry(0, 25, 340, 540)
        self.leftcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.targetfpscontainer = QtWidgets.QFrame(self.leftcontainer)
        self.targetfpscontainer.setGeometry(2, 5, 340, 40)
        self.targetfpscontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.targetfpslabel = QtWidgets.QLabel("Target FPS", self.targetfpscontainer)
        self.targetfpslabel.setGeometry(0, 0, 100, 40)
        self.targetfpslabel.setStyleSheet("color: white; font-size: 12px;")
        self.targetfpsinput = QtWidgets.QLineEdit(self.targetfpscontainer)
        self.targetfpsinput.setGeometry(265, 4, 60, 35)
        self.targetfpsinput.setStyleSheet(inputStyles)
        self.targetfpsinput.setText(str(self.pixelbot_instance.config.targetfps))
        self.inputChangeTimer = QTimer(self)
        self.inputChangeTimer.setSingleShot(True)
        self.inputChangeTimer.timeout.connect(self.changeinputtargetfps)
        self.inputChangeTimer.setInterval(1000)
        self.targetfpsinput.textChanged.connect(lambda: self.inputChangeTimer.start())
        
        self.headoffsetcontiner = QtWidgets.QFrame(self.leftcontainer)
        self.headoffsetcontiner.setGeometry(2, 30, 340, 40)
        self.headoffsetcontiner.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.headoffsetlabel = QtWidgets.QLabel("Head offset", self.headoffsetcontiner)
        self.headoffsetlabel.setGeometry(0, 0, 100, 40)
        self.headoffsetlabel.setStyleSheet("color: white; font-size: 12px;")
        self.headoffsetinput = QtWidgets.QLineEdit(self.headoffsetcontiner)
        self.headoffsetinput.setGeometry(265, 4, 60, 35)
        self.headoffsetinput.setStyleSheet(inputStyles)
        self.headoffsetinput.setText(str(self.pixelbot_instance.config.headoffset))
        self.headoffsetinput.textChanged.connect(self.changeinputHeadOffset)
        
        self.torsooffsetcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.torsooffsetcontainer.setGeometry(2, 55, 340, 40)
        self.torsooffsetcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.torsooffsetlabel = QtWidgets.QLabel("Torso offset", self.torsooffsetcontainer)
        self.torsooffsetlabel.setGeometry(0, 0, 100, 40)
        self.torsooffsetlabel.setStyleSheet("color: white; font-size: 12px;")
        self.torsooffsetinput = QtWidgets.QLineEdit(self.torsooffsetcontainer)
        self.torsooffsetinput.setGeometry(265, 4, 60, 35)
        self.torsooffsetinput.setStyleSheet(inputStyles)
        self.torsooffsetinput.setText(str(self.pixelbot_instance.config.torsooffset))
        self.torsooffsetinput.textChanged.connect(self.changeinputTorsoOffset)
        
        self.legoffsetcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.legoffsetcontainer.setGeometry(2, 80, 340, 40)
        self.legoffsetcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.legoffsetlabel = QtWidgets.QLabel("Legs offset", self.legoffsetcontainer)
        self.legoffsetlabel.setGeometry(0, 0, 100, 40)
        self.legoffsetlabel.setStyleSheet("color: white; font-size: 12px;")
        self.legoffsetinput = QtWidgets.QLineEdit(self.legoffsetcontainer)
        self.legoffsetinput.setGeometry(265, 4, 60, 35)
        self.legoffsetinput.setStyleSheet(inputStyles)
        self.legoffsetinput.setText(str(self.pixelbot_instance.config.legsoffset))
        self.legoffsetinput.textChanged.connect(self.changeinputLegsOffset)
        
        self.penisoffsetcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.penisoffsetcontainer.setGeometry(2, 105, 340, 40)
        self.penisoffsetcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.penisoffsetlabel = QtWidgets.QLabel("Penis offset", self.penisoffsetcontainer)
        self.penisoffsetlabel.setGeometry(0, 0, 100, 40)
        self.penisoffsetlabel.setStyleSheet("color: white; font-size: 12px;")
        self.penisoffsetinput = QtWidgets.QLineEdit(self.penisoffsetcontainer)
        self.penisoffsetinput.setGeometry(265, 4, 60, 35)
        self.penisoffsetinput.setStyleSheet(inputStyles)
        self.penisoffsetinput.setText(str(self.pixelbot_instance.config.penisoffset))
        self.penisoffsetinput.textChanged.connect(self.changeinputPenisOffset)
        
        
        self.rightcontainer = QtWidgets.QFrame(self.panelMisc)
        self.rightcontainer.setGeometry(320, 25, 340, 540)
        self.rightcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
    
class ConfigTab:
    
    def loadMain(self):
        self.panelConfig = QtWidgets.QFrame(self.maincontainer)
        self.panelConfig.setGeometry(0, 0, 660, 545)
        self.panelConfig.setStyleSheet("background-color: rgba(27, 27, 27, 255); margin: 10px; margin-bottom: 5px;")
        self.panelTitle = QtWidgets.QLabel("Config Manager", self.panelConfig)
        self.panelTitle.setGeometry(0, 0, 660, 40)
        self.panelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.panelTitle.setStyleSheet("color: white; font-size: 15px; border-bottom: 1px solid rgba(255, 255, 255, 50);")
    
    def loadContent(self):
        ConfigTab.loadContentConfig(self)
        
    def loadContentConfig(self):
        
        self.config_files = self.pixelbot_instance.getConfigFiles()
        
        self.leftcontainer = QtWidgets.QFrame(self.panelConfig)
        self.leftcontainer.setGeometry(0, 25, 340, 540)
        self.leftcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.configcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.configcontainer.setGeometry(10, 10, 340, 460)
        self.configcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.configlabel = QtWidgets.QLabel("Config List", self.configcontainer)
        self.configlabel.setGeometry(0, 0, 340, 40)
        self.configlabel.setStyleSheet("color: rgba(196, 18, 112, 255); font-size: 12px; background-color: rgba(33, 33, 33, 255)")
        
        for index, config in enumerate(self.config_files):
            configfilelabel = QtWidgets.QLabel(f"{config['filename']}", self.configcontainer)
            configfilelabel.setGeometry(0, 27 + (index * 40), 340, 40)
            configfilelabel.setStyleSheet("color: white; font-size: 12px; background-color: rgba(0, 0, 0, 0);")
        
        self.selectconfigcontainer = QtWidgets.QFrame(self.leftcontainer)
        self.selectconfigcontainer.setGeometry(8, 470, 340, 40)
        self.selectconfigcontainer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.selectconfiglabel = QtWidgets.QLabel("Select config", self.selectconfigcontainer)
        self.selectconfiglabel.setGeometry(0, 0, 150, 40)
        self.selectconfiglabel.setStyleSheet("color: white; font-size: 12px;")
        self.selectconfigcombo = QtWidgets.QComboBox(self.selectconfigcontainer)
        self.selectconfigcombo.setGeometry(100, 0, 230, 40)
        self.selectconfigcombo.setStyleSheet(comboStyles)
        self.selectconfigcombo.setEditable(True)
        
        for config in self.config_files:
            self.selectconfigcombo.addItem(config['filename'])
        
        self.rightcontainer = QtWidgets.QFrame(self.panelConfig)
        self.rightcontainer.setGeometry(320, 25, 340, 540)
        self.rightcontainer.setStyleSheet("background-color: rgba(22, 22, 22, 0); padding: 5px;")
        
        self.loadconfigbutton = QtWidgets.QPushButton("Load Config", self.rightcontainer)
        self.loadconfigbutton.setGeometry(20, 10, 310, 45)
        self.loadconfigbutton.setStyleSheet(buttonStyles)
        self.loadconfigbutton.clicked.connect(self.loadConfigFile)
        
        self.saveconfigbutton = QtWidgets.QPushButton("Save Config", self.rightcontainer)
        self.saveconfigbutton.setGeometry(20, 55, 310, 45)
        self.saveconfigbutton.setStyleSheet(buttonStyles)
        self.saveconfigbutton.clicked.connect(self.saveConfigFile)
        
        self.createconfigbutton = QtWidgets.QPushButton("Create Config", self.rightcontainer)
        self.createconfigbutton.setGeometry(20, 100, 310, 45)
        self.createconfigbutton.setStyleSheet(buttonStyles)
        self.createconfigbutton.clicked.connect(self.createConfigFile)
        
        self.deleteconfigbutton = QtWidgets.QPushButton("Delete Config", self.rightcontainer)
        self.deleteconfigbutton.setGeometry(20, 145, 310, 45)
        self.deleteconfigbutton.setStyleSheet(buttonStyles)
        self.deleteconfigbutton.clicked.connect(self.deleteConfigFile)