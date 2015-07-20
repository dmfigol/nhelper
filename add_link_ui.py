# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_link.ui'
#
# Created: Mon Jun 22 08:48:33 2015
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

class Ui_AddLinkDialog(object):
    def setupUi(self, AddLinkDialog):
        AddLinkDialog.setObjectName(_fromUtf8("AddLinkDialog"))
        AddLinkDialog.resize(372, 154)
        self.buttonBox = QtGui.QDialogButtonBox(AddLinkDialog)
        self.buttonBox.setGeometry(QtCore.QRect(-20, 110, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.uiSlot = QtGui.QLineEdit(AddLinkDialog)
        self.uiSlot.setGeometry(QtCore.QRect(220, 60, 113, 27))
        self.uiSlot.setPlaceholderText(_fromUtf8(""))
        self.uiSlot.setObjectName(_fromUtf8("uiSlot"))
        self.uiTypeLabel = QtGui.QLabel(AddLinkDialog)
        self.uiTypeLabel.setGeometry(QtCore.QRect(60, 20, 111, 21))
        self.uiTypeLabel.setObjectName(_fromUtf8("uiTypeLabel"))
        self.uiSlotLabel = QtGui.QLabel(AddLinkDialog)
        self.uiSlotLabel.setGeometry(QtCore.QRect(60, 60, 161, 21))
        self.uiSlotLabel.setObjectName(_fromUtf8("uiSlotLabel"))
        self.uiType = QtGui.QComboBox(AddLinkDialog)
        self.uiType.setGeometry(QtCore.QRect(190, 20, 151, 27))
        self.uiType.setObjectName(_fromUtf8("uiType"))

        self.retranslateUi(AddLinkDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddLinkDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddLinkDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddLinkDialog)

    def retranslateUi(self, AddLinkDialog):
        AddLinkDialog.setWindowTitle(_translate("AddLinkDialog", "Add link", None))
        self.uiSlot.setText(_translate("AddLinkDialog", "0/0", None))
        self.uiTypeLabel.setText(_translate("AddLinkDialog", "Choose type:", None))
        self.uiSlotLabel.setText(_translate("AddLinkDialog", "Enter slot number:", None))

