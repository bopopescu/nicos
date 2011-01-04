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

"""NICOS "switcher" device."""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"

from nicm.utils import listof, any
from nicm.errors import ConfigurationError, PositionError, NicmError
from nicm.device import Moveable, Readable, Param, Override


class Switcher(Moveable):
    """
    Device that maps switch states onto discrete values of a continuously
    moveable device.
    """

    attached_devices = {
        'moveable': Moveable,
    }

    parameters = {
        'states':    Param('List of state names.', type=listof(str),
                           mandatory=True),
        'values':    Param('List of values to move to', type=listof(any),
                           mandatory=True),
        'precision': Param('Precision for comparison', mandatory=True),
    }

    parameter_overrides = {
        'unit':      Override(mandatory=False),
    }

    def doInit(self):
        states = self.states
        values = self.values
        if len(states) != len(values):
            raise ConfigurationError(self, 'Switcher states and values must be '
                                     'of equal length')
        self._switchlist = dict(zip(states, values))

    def doStart(self, target):
        if target not in self._switchlist:
            positions = ', '.join(repr(pos) for pos in self.states)
            raise NicmError(self, '%r is an invalid position for this device; '
                            'valid positions are %s' % (target, positions))
        target = self._switchlist[target]
        self._adevs['moveable'].start(target)
        self._adevs['moveable'].wait()

    def doRead(self):
        pos = self._adevs['moveable'].read()
        prec = self.precision
        for name, value in self._switchlist.iteritems():
            if prec:
                if abs(pos - value) <= prec:
                    return name
            else:
                if pos == value:
                    return name
        raise PositionError(self, 'unknown position of %s' %
                            self._adevs['moveable'])


class ReadonlySwitcher(Readable):

    attached_devices = {
        'readable': Readable,
    }

    parameters = {
        'states':    Param('List of state names.', type=listof(str),
                           mandatory=True),
        'values':    Param('List of values to move to', type=listof(any),
                           mandatory=True),
        'precision': Param('Precision for comparison', type=float, default=0),
    }

    parameter_overrides = {
        'unit':      Override(mandatory=False),
    }

    def doInit(self):
        states = self.states
        values = self.values
        if len(states) != len(values):
            raise ConfigurationError(self, 'Switcher states and values must be '
                                     'of equal length')
        self._switchlist = dict(zip(states, values))

    def doRead(self):
        pos = self._adevs['readable'].read()
        prec = self.precision
        for name, value in self._switchlist.iteritems():
            if prec:
                if abs(pos - value) <= prec:
                    return name
            else:
                if pos == value:
                    return name
        raise PositionError(self, 'unknown position of %s' %
                            self._adevs['moveable'])
