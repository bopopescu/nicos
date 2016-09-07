#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2016 by the NICOS contributors (see AUTHORS)
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
#   Aleks Wischolit <aleks.wischolit@frm2.tum.de>
#
# *****************************************************************************

"""Readout of FUG power supplies."""

from IO import StringIO

from nicos.core import Readable, Override, status
from nicos.devices.taco.core import TacoDevice


class CurrentA(TacoDevice, Readable):
    taco_class = StringIO

    parameter_overrides = {
        'unit':  Override(mandatory=False, default='A'),
    }

    def doRead(self, maxage=0):
        tmp = self._taco_guard(self._dev.communicate,'N1')
        return float(tmp[:11].strip())

    def doStatus(self, maxage=0):
        return status.OK, ''


class CurrentU(TacoDevice, Readable):

    taco_class = StringIO

    parameter_overrides = {
        'unit':  Override(mandatory=False, default='V'),
    }

    def doRead(self, maxage=0):
        tmp = self._taco_guard(self._dev.communicate,'N0')
        return float(tmp[:11].strip())

    def doStatus(self, maxage=0):
        return status.OK, ''
