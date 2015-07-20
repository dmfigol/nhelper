# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Mon Jun 15 10:03:35 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1513, 951)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.uiWorkAreaContainer = QtGui.QWidget(Form)
        self.uiWorkAreaContainer.setMaximumSize(QtCore.QSize(2000, 750))
        self.uiWorkAreaContainer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.uiWorkAreaContainer.setObjectName(_fromUtf8("uiWorkAreaContainer"))
        self.verticalLayout = QtGui.QVBoxLayout(self.uiWorkAreaContainer)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.uiWorkArea = QtGui.QGraphicsView(self.uiWorkAreaContainer)
        self.uiWorkArea.setEnabled(True)
        self.uiWorkArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.uiWorkArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.uiWorkArea.setObjectName(_fromUtf8("uiWorkArea"))
        self.verticalLayout.addWidget(self.uiWorkArea)
        self.gridLayout.addWidget(self.uiWorkAreaContainer, 1, 1, 1, 1)
        self.uiButtonArea = QtGui.QWidget(Form)
        self.uiButtonArea.setObjectName(_fromUtf8("uiButtonArea"))
        self.uiAddRouterButton = QtGui.QPushButton(self.uiButtonArea)
        self.uiAddRouterButton.setGeometry(QtCore.QRect(110, 80, 112, 34))
        self.uiAddRouterButton.setObjectName(_fromUtf8("uiAddRouterButton"))
        self.uiAddSwitchButton = QtGui.QPushButton(self.uiButtonArea)
        self.uiAddSwitchButton.setGeometry(QtCore.QRect(270, 80, 112, 34))
        self.uiAddSwitchButton.setObjectName(_fromUtf8("uiAddSwitchButton"))
        self.uiAddTemplateButton = QtGui.QPushButton(self.uiButtonArea)
        self.uiAddTemplateButton.setGeometry(QtCore.QRect(720, 80, 112, 34))
        self.uiAddTemplateButton.setObjectName(_fromUtf8("uiAddTemplateButton"))
        self.uiGenerateCfgButton = QtGui.QPushButton(self.uiButtonArea)
        self.uiGenerateCfgButton.setGeometry(QtCore.QRect(1200, 80, 241, 34))
        self.uiGenerateCfgButton.setObjectName(_fromUtf8("uiGenerateCfgButton"))
        self.uiAddLinkButton = QtGui.QToolButton(self.uiButtonArea)
        self.uiAddLinkButton.setGeometry(QtCore.QRect(420, 80, 111, 31))
        self.uiAddLinkButton.setCheckable(True)
        self.uiAddLinkButton.setChecked(False)
        self.uiAddLinkButton.setAutoRaise(False)
        self.uiAddLinkButton.setObjectName(_fromUtf8("uiAddLinkButton"))
        self.uiGlobalOptions = QtGui.QPushButton(self.uiButtonArea)
        self.uiGlobalOptions.setGeometry(QtCore.QRect(1020, 80, 151, 34))
        self.uiGlobalOptions.setObjectName(_fromUtf8("uiGlobalOptions"))
        self.gridLayout.addWidget(self.uiButtonArea, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "nhelper", None))
        self.uiAddRouterButton.setText(_translate("Form", "Add Router", None))
        self.uiAddSwitchButton.setText(_translate("Form", "Add Switch", None))
        self.uiAddTemplateButton.setText(_translate("Form", "Add template", None))
        self.uiGenerateCfgButton.setText(_translate("Form", "Generate configs", None))
        self.uiAddLinkButton.setText(_translate("Form", "Add Link", None))
        self.uiGlobalOptions.setText(_translate("Form", "Global options", None))

