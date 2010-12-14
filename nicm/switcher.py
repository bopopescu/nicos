#  -*- coding: utf-8 -*-
# *****************************************************************************
# Module:
#   $Id$
#
# Description:
#   NICOS "switcher" device
#
# Author:
#   Jens Krüger <jens.krueger@frm2.tum.de>
#
#   The basic NICOS methods for the NICOS daemon (http://nicos.sf.net)
#
#   Copyright (C) 2009 Jens Krüger <jens.krueger@frm2.tum.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# *****************************************************************************

"""NICOS "switcher" device."""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"

from nicm.utils import listof, any
from nicm.errors import ConfigurationError, PositionError
from nicm.device import BaseMoveable, Switchable, Param


class Switcher(Switchable):
    """
    Switchable device that maps switch states onto discrete values of a
    continuously moveable device.
    """

    attached_devices = {
        'moveable': BaseMoveable,
    }

    parameters = {
        'states':    Param('List of state names.', type=listof(str),
                           mandatory=True),
        'values':    Param('List of values to move to', type=listof(any),
                           mandatory=True),
        'precision': Param('Precision for comparison', mandatory=True),
        'unit':      Param('Unit of the device main value', type=str),
    }

    def doInit(self):
        states = self.states
        values = self.values
        if len(states) != len(values):
            raise ConfigurationError(self, 'Switcher states and values must be '
                                     'of equal length')
        self.__dict__['switchlist'] = dict(zip(states, values))

    def doStart(self, target):
        self._adevs['moveable'].start(target)
        self._adevs['moveable'].wait()

    def doRead(self):
        pos = self._adevs['moveable'].read()
        prec = self.precision
        for name, value in self.switchlist.iteritems():
            if prec:
                if abs(pos - value) <= prec:
                    return name
            else:
                if pos == value:
                    return name
        raise PositionError(self, 'unknown position of %s' %
                            self._adevs['moveable'])
