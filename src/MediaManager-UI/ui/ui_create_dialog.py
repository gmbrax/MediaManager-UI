# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_CreateDialog(object):
    def setupUi(self, CreateDialog):
        if not CreateDialog.objectName():
            CreateDialog.setObjectName(u"CreateDialog")
        CreateDialog.resize(785, 94)
        self.gridLayout = QGridLayout(CreateDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.cancelButton = QPushButton(CreateDialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.gridLayout_2.addWidget(self.cancelButton, 0, 2, 1, 1)

        self.okButton = QPushButton(CreateDialog)
        self.okButton.setObjectName(u"okButton")

        self.gridLayout_2.addWidget(self.okButton, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 2, 1, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 0, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 2, 3, 1, 1)

        self.lineEdit = QLineEdit(CreateDialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_3.addWidget(self.lineEdit, 1, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.label = QLabel(CreateDialog)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)


        self.retranslateUi(CreateDialog)

        QMetaObject.connectSlotsByName(CreateDialog)
    # setupUi

    def retranslateUi(self, CreateDialog):
        CreateDialog.setWindowTitle(QCoreApplication.translate("CreateDialog", u"Form", None))
        self.cancelButton.setText(QCoreApplication.translate("CreateDialog", u"Cancel", None))
        self.okButton.setText(QCoreApplication.translate("CreateDialog", u"Ok", None))
        self.label.setText(QCoreApplication.translate("CreateDialog", u"TextLabel", None))
    # retranslateUi

