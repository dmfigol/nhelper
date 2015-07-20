# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'global_options.ui'
#
# Created: Thu Jul  2 03:35:10 2015
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

class Ui_GlobalOptionsDialog(object):
    def setupUi(self, GlobalOptionsDialog):
        GlobalOptionsDialog.setObjectName(_fromUtf8("GlobalOptionsDialog"))
        GlobalOptionsDialog.resize(1016, 1078)
        self.buttonBox = QtGui.QDialogButtonBox(GlobalOptionsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(660, 1030, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(GlobalOptionsDialog)
        self.label.setGeometry(QtCore.QRect(40, 40, 121, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.uiDomainName = QtGui.QLineEdit(GlobalOptionsDialog)
        self.uiDomainName.setGeometry(QtCore.QRect(180, 40, 141, 27))
        self.uiDomainName.setObjectName(_fromUtf8("uiDomainName"))
        self.label_2 = QtGui.QLabel(GlobalOptionsDialog)
        self.label_2.setGeometry(QtCore.QRect(40, 80, 121, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.uiSyslogServer = QtGui.QLineEdit(GlobalOptionsDialog)
        self.uiSyslogServer.setGeometry(QtCore.QRect(180, 80, 141, 27))
        self.uiSyslogServer.setObjectName(_fromUtf8("uiSyslogServer"))
        self.label_3 = QtGui.QLabel(GlobalOptionsDialog)
        self.label_3.setGeometry(QtCore.QRect(40, 120, 121, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.uiNTPServer = QtGui.QLineEdit(GlobalOptionsDialog)
        self.uiNTPServer.setGeometry(QtCore.QRect(180, 120, 141, 27))
        self.uiNTPServer.setObjectName(_fromUtf8("uiNTPServer"))
        self.uiUsername = QtGui.QLineEdit(GlobalOptionsDialog)
        self.uiUsername.setGeometry(QtCore.QRect(280, 240, 141, 27))
        self.uiUsername.setObjectName(_fromUtf8("uiUsername"))
        self.uiPassword = QtGui.QLineEdit(GlobalOptionsDialog)
        self.uiPassword.setGeometry(QtCore.QRect(570, 240, 301, 27))
        self.uiPassword.setObjectName(_fromUtf8("uiPassword"))
        self.label_4 = QtGui.QLabel(GlobalOptionsDialog)
        self.label_4.setGeometry(QtCore.QRect(160, 240, 121, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(GlobalOptionsDialog)
        self.label_5.setGeometry(QtCore.QRect(460, 240, 121, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.uiAddUserButton = QtGui.QPushButton(GlobalOptionsDialog)
        self.uiAddUserButton.setGeometry(QtCore.QRect(360, 300, 112, 34))
        self.uiAddUserButton.setObjectName(_fromUtf8("uiAddUserButton"))
        self.uiLabelMessage = QtGui.QLabel(GlobalOptionsDialog)
        self.uiLabelMessage.setGeometry(QtCore.QRect(360, 210, 371, 21))
        self.uiLabelMessage.setText(_fromUtf8(""))
        self.uiLabelMessage.setObjectName(_fromUtf8("uiLabelMessage"))
        self.uiUsersTable = QtGui.QTableWidget(GlobalOptionsDialog)
        self.uiUsersTable.setGeometry(QtCore.QRect(210, 360, 591, 291))
        self.uiUsersTable.setBaseSize(QtCore.QSize(0, 0))
        self.uiUsersTable.setObjectName(_fromUtf8("uiUsersTable"))
        self.uiUsersTable.setColumnCount(0)
        self.uiUsersTable.setRowCount(0)
        self.uiRemoveUserButton = QtGui.QPushButton(GlobalOptionsDialog)
        self.uiRemoveUserButton.setGeometry(QtCore.QRect(550, 300, 181, 34))
        self.uiRemoveUserButton.setObjectName(_fromUtf8("uiRemoveUserButton"))

        self.retranslateUi(GlobalOptionsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GlobalOptionsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GlobalOptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GlobalOptionsDialog)

    def retranslateUi(self, GlobalOptionsDialog):
        GlobalOptionsDialog.setWindowTitle(_translate("GlobalOptionsDialog", "Global Options", None))
        self.label.setText(_translate("GlobalOptionsDialog", "Domain name:", None))
        self.label_2.setText(_translate("GlobalOptionsDialog", "Syslog server", None))
        self.label_3.setText(_translate("GlobalOptionsDialog", "NTP server", None))
        self.label_4.setText(_translate("GlobalOptionsDialog", "Username:", None))
        self.label_5.setText(_translate("GlobalOptionsDialog", "Password:", None))
        self.uiAddUserButton.setText(_translate("GlobalOptionsDialog", "Add user", None))
        self.uiRemoveUserButton.setText(_translate("GlobalOptionsDialog", "Remove current user", None))

