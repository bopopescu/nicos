#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2019 by the NICOS contributors (see AUTHORS)
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
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#
# *****************************************************************************

"""
Supporting classes for FRM2 magnets, currently only Garfield (amagnet).
"""

from __future__ import absolute_import, division, print_function

from nicos.core import SIMULATION, Attach, CanDisable, HasLimits, Moveable, \
    Override, Param, Readable, dictof, status, tupleof
from nicos.devices.generic import CalibratedMagnet
from nicos.devices.generic.magnet import BipolarSwitchingMagnet
from nicos.devices.generic.sequence import SeqCall, SeqDev, SeqSleep


class GarfieldMagnet(BipolarSwitchingMagnet):
    """Garfield Magnet

    uses a polarity switch ('+' or '-') to flip polarity and an onoff switch
    to cut power (to be able to switch polarity) in addition to an
    unipolar current source.

    Please try to avoid to build anything like this or get headaches!
    Better version would be the MiraMagnet.
    """

    attached_devices = {
        'onoffswitch': Attach('Switch to set for on/off', Moveable),
        'polswitch':   Attach('Switch to set for polarity', Moveable),
        'symmetry':    Attach('Switch to read for symmetry', Moveable),
    }

    parameters = {
        'calibrationtable': Param('Map of coefficients for calibration '
                                  'per symmetry setting',
                                  type=dictof(str, tupleof(
                                      float, float, float, float, float)),
                                  mandatory=True),
    }

    parameter_overrides = {
        'calibration': Override(volatile=True, settable=False,
                                mandatory=False),
    }

    def _getWaiters(self):
        return []

    def doWriteUserlimits(self, limits):
        abslimits = self.abslimits
        # include 0 in limits
        lmin = min(max(limits[0], abslimits[0]), 0)
        lmax = max(min(limits[1], abslimits[1]), 0)
        newlimits = (lmin, lmax)
        self.log.debug('Set limits: %r', newlimits)
        HasLimits.doWriteUserlimits(self, newlimits)
        # intentionally not calling CalibratedMagnet.doWriteUserlimits
        # we do not want to change the limits of the current source
        return newlimits

    def doReadCalibration(self):
        symval = self._attached_symmetry.read()
        return self.calibrationtable.get(symval, (0.0, 0.0, 0.0, 0.0, 0.0))

    def doWriteCalibration(self, cal):
        symval = self._attached_symmetry.read()
        self.calibrationtable[symval] = cal

    def _get_field_polarity(self):
        sign = int(self._attached_polswitch.read())
        if self._attached_onoffswitch.read() == 'off':
            return 0
        return sign

    def doReset(self):
        if self._attached_onoffswitch.status()[0] == status.ERROR:
            self._attached_onoffswitch.reset()
            self._attached_onoffswitch.move('on')
            # immediate action, no need to wait....
        BipolarSwitchingMagnet.doReset(self)
        self._attached_currentsource._dev.On()

    def _seq_set_field_polarity(self, polarity, sequence):
        if polarity == 0:
            return
        pol, onoff = self._attached_polswitch, self._attached_onoffswitch
        # handle switching polarity

        sequence.append(SeqDev(onoff, 'off'))
        sequence.append(SeqSleep(0.3, 'disabling power'))
        sequence.append(SeqDev(pol, '%+d' % polarity))
        sequence.append(SeqSleep(0.3, 'switching polarity'))
        sequence.append(SeqDev(onoff, 'on'))
        sequence.append(SeqSleep(0.3, 'enabling power'))
        sequence.append(SeqCall(self._attached_currentsource._dev.On))
        sequence.append(SeqSleep(0.3, 're-enabling power supply'))

    def doStart(self, target):
        if self._mode != SIMULATION:
            self._attached_onoffswitch._dev.On()
            self._attached_polswitch._dev.On()
            self._attached_symmetry._dev.On()
            self._attached_currentsource._dev.On()
            BipolarSwitchingMagnet.doStart(self, target)


class GarfieldMagnet2(CanDisable, CalibratedMagnet):
    """Garfield Magnet

    Uses a polarity switch ('+' or '-') to flip polarity and an onoff switch
    to cut power (to be able to switch polarity) in addition to an
    unipolar current source.

    Improved version: polarity switching + current ramping now in the PLC,
    similiar to MiraMagnet.
    """

    attached_devices = {
        'currentreadback': Attach('Device to read back actual current',
                                  Readable, optional=True),
        'enable':          Attach('Switch to set for on/off', Moveable),
        'symmetry':        Attach('Switch to read for symmetry', Moveable),
    }

    parameters = {
        'calibrationtable': Param('Map of coefficients for calibration '
                                  'per symmetry setting',
                                  type=dictof(str, tupleof(
                                      float, float, float, float, float)),
                                  mandatory=True),
    }

    parameter_overrides = {
        'calibration': Override(volatile=True, settable=False,
                                mandatory=False),
    }

    def doRead(self, maxage=0):
        if self._attached_currentreadback is not None:
            return self._current2field(
                self._attached_currentreadback.read(maxage))
        return self._current2field(self._attached_currentsource.read(maxage))

    def doWriteUserlimits(self, limits):
        abslimits = self.abslimits
        # include 0 in limits
        lmin = min(max(limits[0], abslimits[0]), 0)
        lmax = max(min(limits[1], abslimits[1]), 0)
        newlimits = (lmin, lmax)
        self.log.debug('Set limits: %r', newlimits)
        HasLimits.doWriteUserlimits(self, newlimits)
        # intentionally not calling CalibratedMagnet.doWriteUserlimits
        # we do not want to change the limits of the current source
        return newlimits

    def doReadCalibration(self):
        symval = self._attached_symmetry.read()
        return self.calibrationtable.get(symval, (0.0, 0.0, 0.0, 0.0, 0.0))

    def doWriteCalibration(self, cal):
        symval = self._attached_symmetry.read()
        self.calibrationtable[symval] = cal

    def doReset(self):
        self.disable()
        self.enable()
        # setting enable to 'on' will clear all errors. (if possible)

    def doStart(self, target):
        self.enable()
        CalibratedMagnet.doStart(self, target)

    def doEnable(self, on):
        # disabling via the enable device will rampdown fast, if needed.
        self._attached_enable.maw('on' if on else 'off')
        self._attached_currentsource.enable() # never disable!
