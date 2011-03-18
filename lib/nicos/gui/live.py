#  -*- coding: utf-8 -*-
# *****************************************************************************
# Module:
#   $Id$
#
# Author:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# NICOS-NG, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
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
# *****************************************************************************

"""NICOS live 2D data plot window."""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignature as qtsig

from nicos.gui.utils import loadUi

import cascadenicoswidget


class LiveWindow(QMainWindow, DlgUtils):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        DlgUtils.__init__(self, 'Live data')
        loadUi(self, 'live.ui')

        self.widget = cascadenicoswidget.CascadeWidget(self)
        self.setCentralWidget(self.widget)

        self.connect(self.actionLogScale, SIGNAL("toggled(bool)"),
                     self.widget, SLOT("SetLog10(bool)"))

    def setData(self, data):
        self.widget.LoadPadMem(data, 128*128*4)
