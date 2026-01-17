# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLayout,
    QMainWindow, QMdiArea, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_MediaManagerMain(object):
    def setupUi(self, MediaManagerMain):
        if not MediaManagerMain.objectName():
            MediaManagerMain.setObjectName(u"MediaManagerMain")
        MediaManagerMain.resize(1024, 769)
        MediaManagerMain.setToolTipDuration(-2)
        MediaManagerMain.setLocale(QLocale(QLocale.English, QLocale.Anguilla))
        MediaManagerMain.setDocumentMode(False)
        MediaManagerMain.setTabShape(QTabWidget.TabShape.Rounded)
        self.actionFolder = QAction(MediaManagerMain)
        self.actionFolder.setObjectName(u"actionFolder")
        self.actionFiles = QAction(MediaManagerMain)
        self.actionFiles.setObjectName(u"actionFiles")
        self.actionExport = QAction(MediaManagerMain)
        self.actionExport.setObjectName(u"actionExport")
        self.actionCut = QAction(MediaManagerMain)
        self.actionCut.setObjectName(u"actionCut")
        self.actionCopy = QAction(MediaManagerMain)
        self.actionCopy.setObjectName(u"actionCopy")
        self.actionPaste = QAction(MediaManagerMain)
        self.actionPaste.setObjectName(u"actionPaste")
        self.actionLIbrary_Viewer = QAction(MediaManagerMain)
        self.actionLIbrary_Viewer.setObjectName(u"actionLIbrary_Viewer")
        self.actionStatistics_View = QAction(MediaManagerMain)
        self.actionStatistics_View.setObjectName(u"actionStatistics_View")
        self.actionTile = QAction(MediaManagerMain)
        self.actionTile.setObjectName(u"actionTile")
        self.actionCascade = QAction(MediaManagerMain)
        self.actionCascade.setObjectName(u"actionCascade")
        self.actionClose_All = QAction(MediaManagerMain)
        self.actionClose_All.setObjectName(u"actionClose_All")
        self.actionClose_Current = QAction(MediaManagerMain)
        self.actionClose_Current.setObjectName(u"actionClose_Current")
        self.actionAbout_Media_Manager = QAction(MediaManagerMain)
        self.actionAbout_Media_Manager.setObjectName(u"actionAbout_Media_Manager")
        self.actionSettings = QAction(MediaManagerMain)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionUndo = QAction(MediaManagerMain)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MediaManagerMain)
        self.actionRedo.setObjectName(u"actionRedo")
        self.centralwidget = QWidget(MediaManagerMain)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.taskTreeWidget = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.taskTreeWidget.setHeaderItem(__qtreewidgetitem)
        self.taskTreeWidget.setObjectName(u"taskTreeWidget")
        self.taskTreeWidget.header().setVisible(False)

        self.gridLayout.addWidget(self.taskTreeWidget, 0, 0, 1, 1)

        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(u"mdiArea")

        self.gridLayout.addWidget(self.mdiArea, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 8)
        self.gridLayout.setColumnMinimumWidth(0, 2)
        self.gridLayout.setColumnMinimumWidth(1, 8)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 2, 1, 1)

        MediaManagerMain.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MediaManagerMain)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 21))
        self.menuLibrary = QMenu(self.menubar)
        self.menuLibrary.setObjectName(u"menuLibrary")
        self.menuIngest = QMenu(self.menuLibrary)
        self.menuIngest.setObjectName(u"menuIngest")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MediaManagerMain.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MediaManagerMain)
        self.statusbar.setObjectName(u"statusbar")
        MediaManagerMain.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuLibrary.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuLibrary.addAction(self.menuIngest.menuAction())
        self.menuLibrary.addAction(self.actionExport)
        self.menuLibrary.addSeparator()
        self.menuIngest.addAction(self.actionFolder)
        self.menuIngest.addAction(self.actionFiles)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionLIbrary_Viewer)
        self.menuView.addAction(self.actionStatistics_View)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionSettings)
        self.menuWindow.addAction(self.actionTile)
        self.menuWindow.addAction(self.actionCascade)
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.actionClose_All)
        self.menuWindow.addAction(self.actionClose_Current)
        self.menuHelp.addAction(self.actionAbout_Media_Manager)

        self.retranslateUi(MediaManagerMain)

        QMetaObject.connectSlotsByName(MediaManagerMain)
    # setupUi

    def retranslateUi(self, MediaManagerMain):
        MediaManagerMain.setWindowTitle(QCoreApplication.translate("MediaManagerMain", u"MediaManager", None))
        self.actionFolder.setText(QCoreApplication.translate("MediaManagerMain", u"Folder", None))
        self.actionFiles.setText(QCoreApplication.translate("MediaManagerMain", u"Files", None))
        self.actionExport.setText(QCoreApplication.translate("MediaManagerMain", u"Backup Library", None))
        self.actionCut.setText(QCoreApplication.translate("MediaManagerMain", u"Cut", None))
        self.actionCopy.setText(QCoreApplication.translate("MediaManagerMain", u"Copy", None))
        self.actionPaste.setText(QCoreApplication.translate("MediaManagerMain", u"Paste", None))
        self.actionLIbrary_Viewer.setText(QCoreApplication.translate("MediaManagerMain", u"LIbrary Viewer", None))
        self.actionStatistics_View.setText(QCoreApplication.translate("MediaManagerMain", u"Statistics Viewer", None))
        self.actionTile.setText(QCoreApplication.translate("MediaManagerMain", u"Tile", None))
        self.actionCascade.setText(QCoreApplication.translate("MediaManagerMain", u"Cascade", None))
        self.actionClose_All.setText(QCoreApplication.translate("MediaManagerMain", u"Close All", None))
        self.actionClose_Current.setText(QCoreApplication.translate("MediaManagerMain", u"Close Current", None))
        self.actionAbout_Media_Manager.setText(QCoreApplication.translate("MediaManagerMain", u"About Media Manager", None))
        self.actionSettings.setText(QCoreApplication.translate("MediaManagerMain", u"Settings", None))
        self.actionUndo.setText(QCoreApplication.translate("MediaManagerMain", u"Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("MediaManagerMain", u"Redo", None))
        self.menuLibrary.setTitle(QCoreApplication.translate("MediaManagerMain", u"Library", None))
        self.menuIngest.setTitle(QCoreApplication.translate("MediaManagerMain", u"Ingest ", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MediaManagerMain", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MediaManagerMain", u"View", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MediaManagerMain", u"Window", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MediaManagerMain", u"Help", None))
    # retranslateUi

