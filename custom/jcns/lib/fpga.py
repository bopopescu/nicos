# -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
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
#   Christian Felder <c.felder@fz-juelich.de>
#
# *****************************************************************************

"""FPGA Counter Card module

This module provides classes for controlling the ZEA-2 FPGA Counter Card using
their own interface. The current implementation does _not_ support multiple
masters, e.g. counting on time and count rate.

"""

import nicos.core.status as status
from nicos.core.params import Param, intrange
from nicos.devices.tango import PyTangoDevice
from nicos.devices.generic import ActiveChannel, TimerChannelMixin, \
    CounterChannelMixin

# XXX: implement doReadIsmaster to determine which channel is actually the
# current master.


class FPGAChannelBase(PyTangoDevice, ActiveChannel):
    """Basic Tango Device for ZEA-2 Counter Card."""

    def _setPreselection(self):
        """This method must be present and should set the the preselection
        value for the card before start."""
        raise NotImplementedError

    def doStart(self):
        self._dev.DevFPGACountReset()
        if self.ismaster:
            # preselection has to be set here and not in doWritePreset
            # because `DevFPGACountReset()` resets all values.
            self._setPreselection()
        self._dev.DevFPGACountStart()

    def doFinish(self):
        self._dev.DevFPGACountStop()

    def doStop(self):
        self.doFinish()

    def doPause(self):
        self.finish()

    def doResume(self):
        self._dev.DevFPGACountStart()

    def doRead(self, maxage=0):
        raise NotImplementedError

    def doStatus(self, maxage=0):
        # Workaround self._dev.State() does not return DevState.MOVING
        if self._dev.DevFPGACountGateStatus():
            res = (status.BUSY, 'counting')
        else:
            res = (status.OK, '')
        return res

    def doReset(self):
        if self.status(0)[0] == status.BUSY:
            self.finish()
        self._dev.DevFPGACountReset()


class FPGATimerChannel(TimerChannelMixin, FPGAChannelBase):
    """FPGATimerChannel implements one time channel for ZEA-2 counter card."""

    def _setPreselection(self):
        millis = int(self.preselection * 1000)
        self._dev.DevFPGACountSetTimeLimit(millis)
        self._dev.DevFPGACountSetMinTime(millis)

    def doRead(self, maxage=0):
        return [self._dev.DevFPGACountReadTime() / 1000.]


class FPGACounterChannel(CounterChannelMixin, FPGAChannelBase):
    """FPGACounterChannel implements one monitor channel for ZEA-2 counter
    card.
    """

    parameters = {
        'channel': Param('Channel number', type=intrange(0, 4),
                         settable=False, mandatory=True)
    }

    def _setPreselection(self):
        self._dev.DevFPGACountSetMinTime(0)
        self._dev.DevFPGACountSetTimeLimit(3600*24)
        self._dev.DevFPGACountSetCountLimit([self.channel,
                                             int(self.preselection)])

    def doRead(self, maxage=0):
        return self._dev.DevFPGACountReadCount(self.channel)
