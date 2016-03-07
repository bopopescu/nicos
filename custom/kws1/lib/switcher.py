#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2015 by the NICOS contributors (see AUTHORS)
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
#   Georg Brandl <g.brandl@fz-juelich.de>
#
# *****************************************************************************

"""Switcher extensions for KWS."""

from nicos.core import Moveable, Attach, Param, Override, oneof, dictof, \
    anytype
from nicos.devices.generic.switcher import MultiSwitcher


class DynamicMultiSwitcher(MultiSwitcher):
    """Switcher whose currently available mapping depends on other devices.

    This is selected by the `_determineMapping` method.
    """

    parameters = {
        'mappings': Param('Collection of mappings',
                          type=dictof(anytype, anytype))
    }

    parameter_overrides = {
        'mapping':  Override(mandatory=False, settable=True, userparam=False),
    }

    def _determineMapping(self):
        raise NotImplementedError('implement _determineMapping')

    def doUpdateMapping(self, newvalue):
        self.valuetype = oneof(*newvalue)

    def doStart(self, target):
        self.mapping = self._determineMapping()
        MultiSwitcher.doStart(self, target)

    def doPoll(self, i, maxage):
        # will use the correct mapping on the next polling cycle
        self._setROParam('mapping', self._determineMapping())


class DetectorPosSwitcher(DynamicMultiSwitcher):
    """Switcher for the detector position.

    This controls the X, Y and Z components of the detector position.  Presets
    depend on the target wavelength given by the selector.
    """

    attached_devices = {
        'selector':  Attach('Selector preset device', Moveable),
    }

    def _determineMapping(self):
        sel_value = self._attached_selector.target
        return self.mappings.get(sel_value, {})


class TofSwitcher(DynamicMultiSwitcher):
    """Switcher for the TOF setting.

    This controls the chopper phase and frequency, as well as the TOF slice
    settings for the detector.  Presets depend on the target wavelength as well
    as the detector position.
    """

    attached_devices = {
        'selector':    Attach('Selector preset switcher', MultiSwitcher),
        'det_pos':     Attach('Detector preset switcher', DetectorPosSwitcher),
    }

    def _determineMapping(self):
        sel_value = self._attached_selector.target
        det_value = self._attached_det_pos.target
        return self.mappings.get((sel_value, det_value), {})
