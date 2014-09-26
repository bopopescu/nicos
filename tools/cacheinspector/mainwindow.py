#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Pascal Neubert <pascal.neubert@frm2.tum.de>
#
# *****************************************************************************

from os import path
from os.path import join
from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMainWindow, QTreeWidgetItem, QMenu, QAction, QDialog, \
    QSpacerItem
from .dialogconnect import DialogConnect
# The pylint errors must be fixed, but later
from .windowwatcher import WindowWatcher    # pylint: disable=F0401
from .cacheaccess import CacheAccess
from .widgetkeyentry import WidgetKeyEntry  # pylint: disable=F0401
from .windowaddkey import WindowAddKey      # pylint: disable=F0401

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        uic.loadUi(join(path.dirname(path.abspath(__file__)), 'ui',
                        'MainWindow.ui'), self)
        self.dialogConnect = DialogConnect(self)
        self.watcherWindow = WindowWatcher(self)
        self.addKeyWindow = WindowAddKey(self)
        self.cacheAccess = CacheAccess()
        self.contextMenuTreeCache = QMenu(self.treeCache)
        self.contextMenuTreeCache.actionAddToWatcher = QAction('Add to Watcher',
                                                    self.contextMenuTreeCache)
        self.contextMenuTreeCache.actionSubscribe = QAction('Subscribe',
                                                    self.contextMenuTreeCache)
        self.treeCache.addAction(self.contextMenuTreeCache.actionAddToWatcher)
        self.treeCache.addAction(self.contextMenuTreeCache.actionSubscribe)
        self.setupEvents()
        self.ipAddress = '127.0.0.1'
        self.port = 14869
        self.TCPconnection = True
        self.progressLoading.hide()
        self.showTimeStamp = False
        self.showTTL = False

    def setupEvents(self):
        """ Sets up all events. """
        self.actionConnect.triggered.connect(self.openConnectDialog)
        self.actionDisconnect.triggered.connect(self.closeConnection)
        self.actionRefresh.triggered.connect(self.refreshAll)
        self.actionQuit.triggered.connect(self.close)
        self.actionAddNewKey.triggered.connect(self.addNewKey)
        self.actionSearch.triggered.connect(self.search)
        self.actionToggleTimeStamp.triggered.connect(self.toggleTimeStamp)
        self.actionToggleTTL.triggered.connect(self.toggleTTL)
        self.actionWatcher.triggered.connect(self.showWatcher)
        # self.comboFilter.editTextChanged.connect(self.updateTree)
        self.buttonSearch.clicked.connect(self.updateTree)
        self.treeCache.itemClicked.connect(self.updateView)
        self.treeCache.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenuTreeCache.actionAddToWatcher.triggered.connect(
            self.addKeyToWatcher)
        self.contextMenuTreeCache.actionSubscribe.triggered.connect(
            self.subscribeKey)

    def openConnectDialog(self):
        """ Opens the connect dialog. """
        self.dialogConnect.show()
        self.dialogConnect.exec_()

    def closeConnection(self):
        """ Closes the connection of the cache inspector. """
        self.actionConnect.setEnabled(True)
        self.actionDisconnect.setDisabled(True)
        self.actionRefresh.setDisabled(True)
        self.clearCacheTree()
        self.clearWidgetView()
        self.cacheAccess.closeConnection()

    def refreshAll(self):
        """ Refreshes local data and the view. """
        self.cacheAccess.requestAll(True)
        self.updateTree()
        #self.updateView(self.treeCache.invisibleRootItem(), 0)
        for item in self.treeCache.selectedItems():
            self.updateView(item, 0)

    def addNewKey(self):
        """ Adds a key using the data given via the add key window. """
        self.addKeyWindow.exec_()
        if self.addKeyWindow.result() == QDialog.Accepted:
            #timeStamp = self.addKeyWindow.dateTimeStamp.text()
            #print timeStamp
            timeStamp = ''
            ttl = self.addKeyWindow.valueTTL.text()
            key = self.addKeyWindow.valueKey.text()
            value = self.addKeyWindow.valueValue.text()
            self.cacheAccess.setKeyValue(key, value, ttl, timeStamp)
            self.addKeyWindow.valueTTL.setText('')
            self.addKeyWindow.valueKey.setText('')
            self.addKeyWindow.valueValue.setText('')

    def search(self):
        self.treeCache.setCurrentItem(self.treeCache.findItems('nicos')[0])

    def toggleTimeStamp(self):
        """
        Toggles whether or not the time stamp is shown and updates the view
        respectively.
        """
        if self.showTimeStamp:
            self.showTimeStamp = False
        else:
            self.showTimeStamp = True
        for item in self.treeCache.selectedItems():
            self.updateView(item, 0)

    def toggleTTL(self):
        """
        Toggles whether or not the time to live is shown and updates the view
        respectively.
        """
        if self.showTTL:
            self.showTTL = False
        else:
            self.showTTL = True
        for item in self.treeCache.selectedItems():
            self.updateView(item, 0)

    def showWatcher(self):
        """ Shows the window of the watcher. """
        self.watcherWindow.show()

    def updateTree(self):
        """ Updates the elements shown in the tree. """
        cursorShape = self.cursor().shape()
        self.setCursor(Qt.BusyCursor)
        self.clearCacheTree()
        root = None
        child = None
        nextChild = None
        strippedEntries = list()
        for i in range(len(self.cacheAccess.entries)):
            strippedEntries.append(self.cacheAccess.entries[i][
                self.cacheAccess.entries[i].find('@') + 1:])
        for entryNum in range(len(strippedEntries)):
            entry = sorted(strippedEntries)[entryNum]
            if len(self.comboFilter.currentText()) == 0 or \
             entry[:entry.find('=')].find(self.comboFilter.currentText()) != -1:
                keys = entry[:entry.find('=')].split('/')
                if not self.treeCache.findItems(keys[0], Qt.MatchExactly):
                    root = QTreeWidgetItem()
                    root.setText(0, keys[0])
                    self.treeCache.addTopLevelItem(root)
                if len(keys) > 2:
                    for i in range(root.childCount()):
                        if root.child(i):
                            if root.child(i).text(0) == keys[1]:
                                break
                    else:
                        child = QTreeWidgetItem()
                        child.setText(0, keys[1])
                        root.addChild(child)
                for level in range(2, len(keys) - 1):
                    temp = root.child(root.childCount() - 1)
                    for i in range(level - 2):
                        temp = temp.child(temp.childCount() - 1)
                    for index in range(temp.childCount()):
                        if temp.child(index):
                            if temp.child(index).text(0) == keys[level]:
                                break
                    else:
                        nextChild = QTreeWidgetItem()
                        nextChild.setText(0, keys[level])
                        temp.addChild(nextChild)
        self.setCursor(cursorShape)

    def updateView(self, keyCategory, column):
        """ Updates the values shown in the right pane. """
        self.clearWidgetView()
        strKey = ''
        item = keyCategory
        while item != None:
            for i in range(self.treeCache.topLevelItemCount()):
                if item != self.treeCache.topLevelItem(i):
                    break
            else:
                strKey = item.text(0) + '/' + strKey
                break
            strKey = item.text(0) + '/' + strKey
            item = item.parent()
        for entry in self.cacheAccess.entries:
            if entry.find(strKey[:-1] + '/') >= 0:
                if entry.find('!') == -1 or entry.find('=') >= 0 and \
                   entry.find('=') < entry.find('!'):
                    key = entry[entry.find(strKey):entry.find('=')]
                    value = entry[entry.find('=') + 1:-1]
                else:
                    key = entry[entry.find(strKey):entry.find('!')]
                    value = entry[entry.find('!') + 1:-1]
                widget = WidgetKeyEntry(self.cacheAccess, entry, key, value,
                                        self.showTimeStamp, self.showTTL)
                self.layoutContent.insertWidget(0, widget)
            else:
                pass
                # insert category separator?

    def showContextMenu(self, position):
        """ Shows the context menu. """
        self.contextMenuTreeCache.exec_(self.treeCache.mapToGlobal(position))

    def addKeyToWatcher(self):
        """ Adds a key to the watcher window. """
        for item in self.treeCache.selectedItems():
            widgetsEntry = ''
            for entry in self.cacheAccess.entries:
                if entry.find(item.text(0)[:-1]):
                    widgetsEntry = entry
            widget = WidgetKeyEntry(self.cacheAccess, widgetsEntry,
                                    item.text(0), '', self.showTimeStamp,
                                    self.showTTL)
            self.watcherWindow.addWidgetKey(widget)

    def subscribeKey(self):
        """ Subscribes a key. """
        strKey = ''
        for item in self.treeCache.selectedItems():
            while item != None:
                for i in range(self.treeCache.topLevelItemCount()):
                    if item != self.treeCache.topLevelItem(i):
                        break
                else:
                    strKey = item.text(0) + '/' + strKey
                    break
                strKey = item.text(0) + '/' + strKey
                item = item.parent()
            self.cacheAccess.subscribeKey(strKey)

    def connectToServer(self, event):
        """ Connects to the cache server with the given information. """
        self.dialogConnect.valueServerAddress.setDisabled(True)
        self.dialogConnect.valuePort.setDisabled(True)
        self.dialogConnect.radioTCP.setDisabled(True)
        self.dialogConnect.radioUDP.setDisabled(True)
        self.actionConnect.setDisabled(True)
        self.ipAddress = self.dialogConnect.valueServerAddress.text()
        self.port = self.dialogConnect.valuePort.text().toInt()[0]
        self.TCPConnection = self.dialogConnect.radioTCP.isChecked()
        self.cacheAccess.connectToServer(self.ipAddress, self.port,
                                         self.TCPconnection, 5)
        if self.cacheAccess.isConnected():
            self.actionDisconnect.setEnabled(True)
            self.actionRefresh.setEnabled(True)
            self.dialogConnect.close()
            self.dialogConnect.valueServerAddress.setEnabled(True)
            self.dialogConnect.valuePort.setEnabled(True)
            self.dialogConnect.radioTCP.setEnabled(True)
            self.dialogConnect.radioUDP.setEnabled(True)
            self.cacheAccess.requestAll(True)
            self.updateTree()
        else:
            self.actionConnect.setEnabled(True)
            self.dialogConnect.valueServerAddress.setEnabled(True)
            self.dialogConnect.valuePort.setEnabled(True)
            self.dialogConnect.radioTCP.setEnabled(True)
            self.dialogConnect.radioUDP.setEnabled(True)

    def clearCacheTree(self):
        """ Removes all elements in the tree. """
        self.treeCache.clear()

    def clearWidgetView(self):
        """ Removes all widgets in the right pane. """
        for i in reversed(range(self.layoutContent.count())):
            if not isinstance(self.layoutContent.itemAt(i), QSpacerItem):
                self.layoutContent.itemAt(i).widget().setParent(None)
