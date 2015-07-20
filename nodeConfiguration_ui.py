# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NodeConfiguration.ui'
#
# Created: Thu Jul  2 09:01:09 2015
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

class Ui_NodeConfigurationDialog(object):
    def setupUi(self, NodeConfigurationDialog):
        NodeConfigurationDialog.setObjectName(_fromUtf8("NodeConfigurationDialog"))
        NodeConfigurationDialog.resize(1080, 1097)
        self.buttonBox = QtGui.QDialogButtonBox(NodeConfigurationDialog)
        self.buttonBox.setGeometry(QtCore.QRect(820, 1050, 241, 32))
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(NodeConfigurationDialog)
        self.label.setGeometry(QtCore.QRect(40, 40, 91, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.uiHostname = QtGui.QLineEdit(NodeConfigurationDialog)
        self.uiHostname.setGeometry(QtCore.QRect(140, 40, 111, 27))
        self.uiHostname.setObjectName(_fromUtf8("uiHostname"))
        self.label_2 = QtGui.QLabel(NodeConfigurationDialog)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 70, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(NodeConfigurationDialog)
        self.label_3.setGeometry(QtCore.QRect(40, 130, 70, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.uiType = QtGui.QComboBox(NodeConfigurationDialog)
        self.uiType.setGeometry(QtCore.QRect(140, 90, 111, 27))
        self.uiType.setObjectName(_fromUtf8("uiType"))
        self.uiVendor = QtGui.QComboBox(NodeConfigurationDialog)
        self.uiVendor.setGeometry(QtCore.QRect(140, 130, 111, 27))
        self.uiVendor.setObjectName(_fromUtf8("uiVendor"))
        self.uiRouting = QtGui.QCheckBox(NodeConfigurationDialog)
        self.uiRouting.setGeometry(QtCore.QRect(510, 40, 131, 25))
        self.uiRouting.setObjectName(_fromUtf8("uiRouting"))
        self.label_4 = QtGui.QLabel(NodeConfigurationDialog)
        self.label_4.setGeometry(QtCore.QRect(640, 220, 51, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.uiPrefix = QtGui.QLineEdit(NodeConfigurationDialog)
        self.uiPrefix.setGeometry(QtCore.QRect(610, 250, 131, 27))
        self.uiPrefix.setObjectName(_fromUtf8("uiPrefix"))
        self.uiTabWidget = QtGui.QTabWidget(NodeConfigurationDialog)
        self.uiTabWidget.setGeometry(QtCore.QRect(50, 640, 991, 391))
        self.uiTabWidget.setObjectName(_fromUtf8("uiTabWidget"))
        self.uiAddInterfaceButton = QtGui.QPushButton(NodeConfigurationDialog)
        self.uiAddInterfaceButton.setGeometry(QtCore.QRect(610, 590, 121, 34))
        self.uiAddInterfaceButton.setObjectName(_fromUtf8("uiAddInterfaceButton"))
        self.uiInterfaceNumber = QtGui.QLineEdit(NodeConfigurationDialog)
        self.uiInterfaceNumber.setGeometry(QtCore.QRect(520, 590, 61, 27))
        self.uiInterfaceNumber.setText(_fromUtf8(""))
        self.uiInterfaceNumber.setObjectName(_fromUtf8("uiInterfaceNumber"))
        self.uiInterfaceType = QtGui.QComboBox(NodeConfigurationDialog)
        self.uiInterfaceType.setGeometry(QtCore.QRect(340, 590, 161, 27))
        self.uiInterfaceType.setObjectName(_fromUtf8("uiInterfaceType"))
        self.label_5 = QtGui.QLabel(NodeConfigurationDialog)
        self.label_5.setGeometry(QtCore.QRect(350, 550, 111, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(NodeConfigurationDialog)
        self.label_6.setGeometry(QtCore.QRect(500, 550, 131, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.uiOSPF = QtGui.QCheckBox(NodeConfigurationDialog)
        self.uiOSPF.setGeometry(QtCore.QRect(510, 110, 141, 25))
        self.uiOSPF.setObjectName(_fromUtf8("uiOSPF"))
        self.uiEIGRP = QtGui.QCheckBox(NodeConfigurationDialog)
        self.uiEIGRP.setGeometry(QtCore.QRect(510, 80, 104, 25))
        self.uiEIGRP.setObjectName(_fromUtf8("uiEIGRP"))
        self.uiOSPFProcess = QtGui.QLineEdit(NodeConfigurationDialog)
        self.uiOSPFProcess.setGeometry(QtCore.QRect(650, 110, 151, 27))
        self.uiOSPFProcess.setObjectName(_fromUtf8("uiOSPFProcess"))
        self.uiEIGRP_AS = QtGui.QLineEdit(NodeConfigurationDialog)
        self.uiEIGRP_AS.setGeometry(QtCore.QRect(620, 80, 151, 27))
        self.uiEIGRP_AS.setObjectName(_fromUtf8("uiEIGRP_AS"))
        self.uiStaticRoutesTable = QtGui.QTableWidget(NodeConfigurationDialog)
        self.uiStaticRoutesTable.setGeometry(QtCore.QRect(120, 230, 391, 291))
        self.uiStaticRoutesTable.setObjectName(_fromUtf8("uiStaticRoutesTable"))
        self.uiStaticRoutesTable.setColumnCount(0)
        self.uiStaticRoutesTable.setRowCount(0)
        self.label_7 = QtGui.QLabel(NodeConfigurationDialog)
        self.label_7.setGeometry(QtCore.QRect(260, 190, 131, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.uiNexthop = QtGui.QLineEdit(NodeConfigurationDialog)
        self.uiNexthop.setGeometry(QtCore.QRect(790, 250, 131, 27))
        self.uiNexthop.setText(_fromUtf8(""))
        self.uiNexthop.setObjectName(_fromUtf8("uiNexthop"))
        self.label_8 = QtGui.QLabel(NodeConfigurationDialog)
        self.label_8.setGeometry(QtCore.QRect(780, 220, 161, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.uiAddStaticRouteButton = QtGui.QPushButton(NodeConfigurationDialog)
        self.uiAddStaticRouteButton.setGeometry(QtCore.QRect(680, 290, 151, 34))
        self.uiAddStaticRouteButton.setObjectName(_fromUtf8("uiAddStaticRouteButton"))
        self.uiRemoveStaticRouteButton = QtGui.QPushButton(NodeConfigurationDialog)
        self.uiRemoveStaticRouteButton.setGeometry(QtCore.QRect(640, 330, 241, 34))
        self.uiRemoveStaticRouteButton.setObjectName(_fromUtf8("uiRemoveStaticRouteButton"))

        self.retranslateUi(NodeConfigurationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NodeConfigurationDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NodeConfigurationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NodeConfigurationDialog)

    def retranslateUi(self, NodeConfigurationDialog):
        NodeConfigurationDialog.setWindowTitle(_translate("NodeConfigurationDialog", "Device Configuration", None))
        self.label.setText(_translate("NodeConfigurationDialog", "Hostname: ", None))
        self.label_2.setText(_translate("NodeConfigurationDialog", "Type", None))
        self.label_3.setText(_translate("NodeConfigurationDialog", "Vendor", None))
        self.uiRouting.setText(_translate("NodeConfigurationDialog", "IPv4 routing", None))
        self.label_4.setText(_translate("NodeConfigurationDialog", "Prefix", None))
        self.uiPrefix.setText(_translate("NodeConfigurationDialog", "0.0.0.0/0", None))
        self.uiAddInterfaceButton.setText(_translate("NodeConfigurationDialog", "Add Interface", None))
        self.label_5.setText(_translate("NodeConfigurationDialog", "Interface type", None))
        self.label_6.setText(_translate("NodeConfigurationDialog", "Interface number", None))
        self.uiOSPF.setText(_translate("NodeConfigurationDialog", "OSPF process", None))
        self.uiEIGRP.setText(_translate("NodeConfigurationDialog", "EIGRP AS", None))
        self.uiOSPFProcess.setText(_translate("NodeConfigurationDialog", "1", None))
        self.uiEIGRP_AS.setText(_translate("NodeConfigurationDialog", "1", None))
        self.label_7.setText(_translate("NodeConfigurationDialog", "Static Routing", None))
        self.label_8.setText(_translate("NodeConfigurationDialog", "Nexthop or interface", None))
        self.uiAddStaticRouteButton.setText(_translate("NodeConfigurationDialog", "Add static route", None))
        self.uiRemoveStaticRouteButton.setText(_translate("NodeConfigurationDialog", "Remove current static route", None))

