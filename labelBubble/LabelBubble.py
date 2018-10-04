# -*- coding: utf-8 -*-
import codecs
import distutils.spawn
import os.path
import platform
import re
import sys
import subprocess

from functools import partial
from collections import defaultdict

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

    # import resources

# add internal libs
from libs.constants import *
from libs.lib import struct, newAction, newIcon, addActions, fmtShortcut, generateColorByText
from libs.settings import Settings
# from libs.shape import Shape, DEFAULT_LINE_COLOR, DEFAULT_FILL_COLOR
# from libs.canvas import Canvas
from libs.zoomWidget import ZoomWidget
# from libs.labelDialog import LabelDialog
# from libs.colorDialog import ColorDialog
# from libs.labelFile import LabelFile, LabelFileError
from libs.toolBar import ToolBar
# from libs.pascal_voc_io import PascalVocReader
# from libs.pascal_voc_io import XML_EXT
# from libs.yolo_io import YoloReader
# from libs.yolo_io import TXT_EXT
from libs.ustr import ustr
from libs.version import __version__

__appname__ = 'labelBubble'

# Utility functions and classes.

def have_qstring():
    '''p3/qt5 get rid of QString wrapper as py3 has native unicode str type'''
    return not (sys.version_info.major >= 3 or QT_VERSION_STR.startswith('5.'))

def util_qt_strlistclass():
    return QStringList if have_qstring() else list


class WindowMixin(object):

    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            addActions(menu, actions)
        return menu

    def toolbar(self, title, actions=None):
        toolbar = ToolBar(title)
        toolbar.setObjectName(u'%sToolBar' % title)
        # toolbar.setOrientation(Qt.Vertical)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if actions:
            addActions(toolbar, actions)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        return toolbar


# PyQt5: TypeError: unhashable type: 'QListWidgetItem'
class HashableQListWidgetItem(QListWidgetItem):

    def __init__(self, *args):
        super(HashableQListWidgetItem, self).__init__(*args)

    def __hash__(self):
        return hash(id(self))


class MainWindow(QMainWindow, WindowMixin):
    # FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))
    def __init__(self, defaultFilename=None, defaultPrefdefClassFile=None, defaultSaveDir=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle(__appname__)

        # # Load setting in the main thread
        self.settings = Settings()
        self.settings.load()
        settings = self.settings

        # # Save as Pascal voc xml
        # self.defaultSaveDir = defaultSaveDir
        # self.usingPascalVocFormat = True
        # self.usingYoloFormat = False

        # For loading all image under a directory
        self.mImgList = []
        self.dirname = None
        self.labelHist = []
        self.lastOpenDir = None

        # Whether we need to save or not.
        self.dirty = False

        # self._noSelectionSlot = False
        # self._beginner = True
        # self.screencastViewer = self.getAvailableScreencastViewer()
        # self.screencast = "https://youtu.be/p0nR2YsCY_U"

        # Load predefined classes to the list

        # self.loadPredefinedClasses(defaultPrefdefClassFile)

        # Main widgets and related state.

        # self.labelDialog = LabelDialog(parent=self, listItem=self.labelHist)

        # self.itemsToShapes = {}
        # self.shapesToItems = {}
        # self.prevLabelText = ''

        listLayout = QVBoxLayout()
        listLayout.setContentsMargins(0, 0, 0, 0)

        # Create a widget for using default label

        # self.useDefaultLabelCheckbox = QCheckBox(u'Use default label')
        # self.useDefaultLabelCheckbox.setChecked(False)
        # self.defaultLabelTextLine = QLineEdit()
        # useDefaultLabelQHBoxLayout = QHBoxLayout()
        # useDefaultLabelQHBoxLayout.addWidget(self.useDefaultLabelCheckbox)
        # useDefaultLabelQHBoxLayout.addWidget(self.defaultLabelTextLine)
        # useDefaultLabelContainer = QWidget()
        # useDefaultLabelContainer.setLayout(useDefaultLabelQHBoxLayout)

        # Create a widget for edit and diffc button

        self.diffcButton = QCheckBox(u'difficult')
        self.diffcButton.setChecked(False)
        # self.diffcButton.stateChanged.connect(self.btnstate)
        self.editButton = QToolButton()
        # self.editButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # Add some of widgets to listLayout

        listLayout.addWidget(self.editButton)
        listLayout.addWidget(self.diffcButton)
        listLayout.addWidget(useDefaultLabelContainer)


        # Create and add a widget for showing current label items

        self.labelList = QListWidget()
        # self.labelList.itemActivated.connect(self.labelSelectionChanged)
        # self.labelList.itemSelectionChanged.connect(self.labelSelectionChanged)
        # self.labelList.itemDoubleClicked.connect(self.editLabel)
        # # Connect to itemChanged to detect checkbox changes.
        # self.labelList.itemChanged.connect(self.labelItemChanged)
        listLayout.addWidget(self.labelList)

        labelListContainer = QWidget()
        labelListContainer.setLayout(listLayout)
        self.dock = QDockWidget(u'Box Labels', self)
        self.dock.setObjectName(u'Labels')
        self.dock.setWidget(labelListContainer) 

        # Tzutalin 20160906 : Add file list and dock to move faster

        # self.fileListWidget = QListWidget()
        # self.fileListWidget.itemDoubleClicked.connect(self.fileitemDoubleClicked)
        # filelistLayout = QVBoxLayout()
        # filelistLayout.setContentsMargins(0, 0, 0, 0)
        # filelistLayout.addWidget(self.fileListWidget)
        # fileListContainer = QWidget()
        # fileListContainer.setLayout(filelistLayout)
        # self.filedock = QDockWidget(u'File List', self)
        # self.filedock.setObjectName(u'Files')
        # self.filedock.setWidget(fileListContainer)

        # self.zoomWidget = ZoomWidget()
        # self.colorDialog = ColorDialog(parent=self)

        # self.canvas = Canvas(parent=self)
        # self.canvas.zoomRequest.connect(self.zoomRequest)

        # scroll = QScrollArea()
        # scroll.setWidget(self.canvas)
        # scroll.setWidgetResizable(True)
        # self.scrollBars = {
        #     Qt.Vertical: scroll.verticalScrollBar(),
        #     Qt.Horizontal: scroll.horizontalScrollBar()
        # }
        # self.scrollArea = scroll
        # self.canvas.scrollRequest.connect(self.scrollRequest)

        # self.canvas.newShape.connect(self.newShape)
        # self.canvas.shapeMoved.connect(self.setDirty)
        # self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
        # self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

        # self.setCentralWidget(scroll)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        # self.dockFeatures = QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable
        # self.dock.setFeatures(self.dock.features() ^ self.dockFeatures)
        # # Tzutalin 20160906 : Add file list and dock to move faster
        # self.addDockWidget(Qt.RightDockWidgetArea, self.filedock)
        # self.filedock.setFeatures(QDockWidget.DockWidgetFloatable)

        # Actions
        action = partial(newAction, self)
        quit = action('&Quit', self.close,
                      'Ctrl+Q', 'quit', u'Quit application')

        open = action('&Open', self.openFile,
                      'Ctrl+O', 'open', u'Open image or label file')

        opendir = action('&Open Dir', self.openDirDialog,
                         'Ctrl+u', 'open', u'Open Dir')

        changeSavedir = action('&Change Save Dir', self.changeSavedirDialog,
                               'Ctrl+r', 'open', u'Change default saved Annotation dir')

        openAnnotation = action('&Open Annotation', self.openAnnotationDialog,
                                'Ctrl+Shift+O', 'open', u'Open Annotation')

    def close():
        pass
    
    def openFile():
        pass
    


def inverted(color):
    return QColor(*[255 - v for v in color.getRgb()])


def read(filename, default=None):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except:
        return default


def get_main_app(argv=[]):
    """
    Standard boilerplate Qt application code.
    Do everything but app.exec_() -- so that we can test the application in one thread
    """
    app = QApplication(argv)
    app.setApplicationName(__appname__)
    app.setWindowIcon(newIcon("app"))
    # Tzutalin 201705+: Accept extra agruments to change predefined class file
    # Usage : labelImg.py image predefClassFile saveDir
    win = MainWindow(argv[1] if len(argv) >= 2 else None,
                     argv[2] if len(argv) >= 3 else os.path.join(
                         os.path.dirname(sys.argv[0]),
                         'data', 'predefined_classes.txt'),
                     argv[3] if len(argv) >= 4 else None)
    win.show()
    return app, win


def main():
    '''construct main app and run it'''
    app, _win = get_main_app(sys.argv)
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())