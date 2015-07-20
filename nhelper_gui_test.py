#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import form_ui
import nodeConfiguration_ui
import global_options_ui
import add_link_ui
import sys
import nhelper
import re

INTERFACE_RE = re.compile(r'^([a-zA-Z]+)(.+)$')

class MyWindow(QtGui.QWidget, form_ui.Ui_Form):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.scene = QtGui.QGraphicsScene(self.uiWorkArea)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 1200, 600))
        #self.scene.setSceneRect(0, 0, 1200, 600)
        self.uiWorkArea.setScene(self.scene)
        self.uiWorkArea.setMouseTracking(True)
        self.offset_x = 0
        self.offset_y = 0
        self.distance_x = 150
        self.distance_y = 90
        self.next_router_id = 1
        self.next_switch_id = 1
        self.current_node = None
        self.next_link_id = 1
        #self.uiWorkArea.fitInView(pixItem)
        #self.scene.addPixmap(image)
        # for i in range(5):
        #     item = QtGui.QGraphicsEllipseItem(i*200, 10, 60, 40)
        #     self.scene.addItem(item)
        self.uiAddRouterButton.clicked.connect(self.uiAddRouterButton_clicked)
        self.uiAddSwitchButton.clicked.connect(self.uiAddSwitchButton_clicked)
        self.uiAddLinkButton.clicked.connect(self.uiAddLinkButton_clicked)
        self.uiGlobalOptions.clicked.connect(self.uiGlobalOptions_clicked)
        self.label_font =  QtGui.QFont('Arial', 10, QtGui.QFont.Light)
        # self.uiWorkArea.mouseReleaseEvent = self.uiWorkAreaMouseReleaseEvent
        #self.uiWorkArea.mouseMoveEvent = self.uiWorkAreaMouseMoveEvent


    def uiGlobalOptions_clicked(self):
        dialog = GlobalOptionsDialog(self)
        #dialog.exec_()
        dialog.show()

    def uiAddLinkButton_clicked(self):
        if self.uiAddLinkButton.isChecked():
            for item in self.scene.items():
                item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        else:
            if self.current_node and self.current_node.device.interfaces:
                self.current_node.device.interfaces.pop()
                self.current_node = None
            for item in self.scene.items():
                item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)

    def device_clicked(self, event):
        if self.uiAddLinkButton.isChecked():
            print("device clicked")
        else:
            pass

    def add_device(self, device_type="router"):
        image = QtGui.QPixmap("icons/{}_new.png".format(device_type)).scaled(100, 64, transformMode=QtCore.Qt.SmoothTransformation)
        #pixItem = QtGui.QGraphicsPixmapItem(image)
        pix_item = GraphicsItem(image, form=self)
        if device_type =='router':
            device_id = 'R{}'.format(self.next_router_id)
            device = nhelper.Router(device_id)
            pix_item.id = device_id
            pix_item.type = device_type
            self.next_router_id += 1
        elif device_type == 'switch':
            device_id = 'SW{}'.format(self.next_switch_id)
            device = nhelper.Switch(device_id)
            pix_item.id = device_id
            pix_item.type = device_type
            self.next_switch_id += 1
        pix_item.device = device
        if self.offset_x > 1200:
            self.offset_x = 0
            self.offset_y += self.distance_y
        pix_item.setPos(self.offset_x, self.offset_y)
        text = QtGui.QGraphicsTextItem(device_id, parent=pix_item)
        text.setFont(self.label_font)
        text.setPos(35, -30)
        text.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        text.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        #text.setOff
        self.offset_x += self.distance_x
        pix_item.label = text
        pix_item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        pix_item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        #pix_item.mousePressEvent = self.device_clicked
        pix_item.setZValue(100)
        self.scene.addItem(pix_item)

    def uiAddRouterButton_clicked(self):
        self.add_device('router')

    def uiAddSwitchButton_clicked(self):
        self.add_device('switch')

    def uiWorkAreaMouseReleaseEvent(self, event):
        print("pressed")
        self.start = self.uiWorkArea.mapToScene(event.pos())
        print(self.start)


class GlobalOptionsDialog(QtGui.QDialog, global_options_ui.Ui_GlobalOptionsDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def accept(self):
        self.hide()


class AddLinkDialog(QtGui.QDialog, add_link_ui.Ui_AddLinkDialog):
    def __init__(self, form=None, device=None):
        QtGui.QDialog.__init__(self, form)
        self.setupUi(self)
        self.device = device
        self.form = form

    def accept(self):
        interface_name = '{}{}'.format(self.uiType.currentText(),
                                       self.uiSlot.text())
        interface = nhelper.Interface(name=interface_name)
        if self.device.device.interfaces and self.device.device.interfaces[-1] == interface:
            QtGui.QMessageBox.about(self, "My message box", "This interface is already used!")
        else:
            self.device.device.add_interface(interface)
            self.hide()
            if self.form.current_node is None:
                self.form.current_node = self.device
            else:
                line = Line(self.form.current_node, self.device, form=self.form)
                self.form.current_node.links.append(line)
                self.device.links.append(line)
                self.form.scene.addItem(line)
                self.form.current_node = None


    def reject(self):
        self.hide()

class NodeConfigurationDialog(QtGui.QDialog, nodeConfiguration_ui.Ui_NodeConfigurationDialog):
    def __init__(self, parent=None, device=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.device = device

    def accept(self):
        self.device.id = self.uiHostname.text()
        self.device.label.setPlainText(self.uiHostname.text())
        self.hide()


    def reject(self):
        self.hide()

class GraphicsItem(QtGui.QGraphicsPixmapItem):
    def __init__(self, pixmap, parent=None, scene=None, form=None):
        super().__init__(pixmap, parent, scene)
        self.form = form
        self.links = []
        self.device = None
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.form.uiAddLinkButton.isChecked():
            if self.form.current_node == self:
                self.form.current_node = None
                if self.device.interfaces:
                    self.device.interfaces.pop()
            else:
                dialog = AddLinkDialog(self.form, self)
                for interface in nhelper.INTERFACES:
                    dialog.uiType.addItem(interface)
                if self.form.current_node:
                    interface_name = self.form.current_node.device.interfaces[-1].name
                    match = INTERFACE_RE.match(interface_name)
                    type, slot = match.group(1), match.group(2)
                    dialog.uiType.setCurrentIndex(dialog.uiType.findText(type))
                    dialog.uiSlot.setText(slot)
                dialog.show()


    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        for link in self.links:
            link.moving_line()

    def mouseDoubleClickEvent(self, event):
        dialog = NodeConfigurationDialog(self.form, self)
        dialog.uiHostname.setText(self.id)
        dialog.uiType.addItem('router')
        dialog.uiType.addItem('switch')
        dialog.uiType.setCurrentIndex(dialog.uiType.findText(self.type))
        dialog.uiVendor.addItem('cisco')
        #dialog.exec_()
        dialog.show()

    def drawLine(self):
        print("drawing line")
        start_node_size = self.form.current_node.boundingRect().size()
        start = self.form.current_node.pos() + \
                QtCore.QPointF(start_node_size.width()/2, start_node_size.height()/2)
        end_node_size = self.boundingRect().size()
        end = self.pos() + \
                QtCore.QPointF(end_node_size.width()/2, end_node_size.height()/2)
        pen = QtGui.QPen()
        pen.setWidth(3)
        line = QtGui.QGraphicsLineItem(QtCore.QLineF(start, end))
        line.setPen(pen)
        line.setZValue(-200)
        return line

class Line(QtGui.QGraphicsLineItem):
    def __init__(self, start, end, form=None, *args):
        super(Line, self).__init__(*args)
        self.form = form
        self.id = form.next_link_id
        form.next_link_id += 1
        self.start = start
        self.end = end
        self.start_node_size = start.boundingRect().size()
        self.start_pos = start.pos() + \
                QtCore.QPointF(self.start_node_size.width()/2, self.start_node_size.height()/2)
        self.end_node_size = end.boundingRect().size()
        self.end_pos = end.pos() + \
                QtCore.QPointF(self.end_node_size.width()/2, self.end_node_size.height()/2)
        pen = QtGui.QPen()
        pen.setWidth(3)
        self.setPen(pen)
        self.setZValue(-10)
        self.setLine(QtCore.QLineF(self.start_pos, self.end_pos))

    def moving_line(self):
        self.start_pos = self.start.pos() + \
            QtCore.QPointF(self.start_node_size.width()/2, self.start_node_size.height()/2)
        self.end_pos = self.end.pos() + \
            QtCore.QPointF(self.end_node_size.width()/2, self.end_node_size.height()/2)
        self.setLine(QtCore.QLineF(self.start_pos, self.end_pos))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
