#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2020 by the NICOS contributors (see AUTHORS)
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
#   Nikhil Biyani <nikhil.biyani@psi.ch>
#
# *****************************************************************************
"""Astrium chopper devices via EPICS."""

from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from nicos.core import ADMIN, Attach, ConfigurationError, HasPrecision, \
    Override, Param, Readable, UsageError, pvname, requires, status

from nicos_ess.devices.epics.base import EpicsDeviceEss, \
    EpicsDigitalMoveableEss, EpicsWindowTimeoutDeviceEss


class EpicsChopperSpeed(EpicsWindowTimeoutDeviceEss):
    """Used to represent speed setter for the chopper
    """
    valuetype = int


class EpicsChopperDisc(EpicsDeviceEss, Readable):
    """Class that represents one of the chopper disc in the
    chopper system. The chopper disk can be either MASTER
    or a SLAVE. In case it is main, one should be able to
    set the speed and in case it is a subordinate, the ratio and
    phase values can be set for the disc.

    Other parameters such as water flow, temperature, vacuum,
    loss current can also be seen in the formatted value of the
    device.
    """

    parameters = {
        'basepv': Param('Base PV name of the chopper disc',
                        type=pvname, mandatory=True, settable=False,
                        userparam=False),
        'speed': Param('Frequency of the chopper disc', type=int,
                       settable=True, volatile=True, userparam=False),
        'phase': Param('Phase of the chopper disc', type=int,
                       settable=True, volatile=True, userparam=False),
        'ratio': Param('Frequency ratio of the chopper disc to main',
                       type=int, settable=True, volatile=True,
                       userparam=False),
    }

    parameter_overrides = {
        'fmtstr': Override(volatile=True, userparam=False),
        'unit': Override(mandatory=False, userparam=False),
        'maxage': Override(userparam=False),
        'pollinterval': Override(userparam=False),
        'warnlimits': Override(userparam=False)
    }

    attached_devices = {
        'speed': Attach('Device to set the speed if main',
                        EpicsWindowTimeoutDeviceEss, optional=True),
        'phase': Attach('Device to set the phase if subordinate',
                        EpicsWindowTimeoutDeviceEss, optional=True),
        'ratio': Attach('Device to set the speed ratio if subordinate',
                        EpicsDigitalMoveableEss, optional=True),
    }

    # Represents all the associated property values of the disc,
    # An ordered dictionary provides a fixed order of the keys
    # which is used while displaying the properties
    properties = OrderedDict(
        [('state', 'State',),
         ('speed', 'ActSpd',),
         ('phase', 'ActPhs',),
         ('ratio', 'Ratio',),
         ('loss_curr', 'LossCurr',),
         ('vibration', 'Vibration',),
         ('temperature', 'Temp',),
         ('water_flow', 'WaterFlow',),
         ('vacuum', 'Vacuum',),
         ('valve', 'Valve',),
         ('sum_signal', 'SumSignal',)]
    )

    def _get_pv_parameters(self):
        return set(self.properties.keys())

    def _get_pv_name(self, pvparam):
        if pvparam in self.properties:
            return '.'.join((self.basepv, self.properties[pvparam]))

        return getattr(self, pvparam)

    def _get_pv_fmtstr(self, pvparam):
        # Returns the current value along with the units from PVs
        fmt = '%s'
        if pvparam in self.properties:
            fmt += ' ' + self._get_pvctrl(pvparam, 'units', '')
        return fmt

    def _displayed_props(self):
        # Just display the speed and phase in read, rest are in info
        if self.isMain:
            # Phase is not relevant for main
            return ['speed']
        return ['speed', 'phase']

    def doRead(self, maxage=0):
        # List of all string converted values from properties key list
        return [str(self._get_pv(prop)) for prop in self._displayed_props()]

    def doInfo(self):
        ret = []
        for prop in self.properties.keys():
            ret.append((prop,
                        self._get_pv(prop),
                        '%s' % self._get_pv(prop),
                        '%s' % self._get_pvctrl(prop, 'units', ''),
                        'general'))
        return ret

    def doReadFmtstr(self):
        return ', '.join(' %s' % (self._get_pv_fmtstr(v)) for v in
                         self._displayed_props())

    def doStatus(self, maxage=0):
        if EpicsDeviceEss.doStatus(self, maxage)[0] == status.ERROR:
            return EpicsDeviceEss.doStatus(self, maxage)

        if (self._attached_speed
                and self._attached_speed.status(maxage)[0] == status.BUSY):
            return status.BUSY, 'Speed moving to target'

        if (self._attached_phase
                and self._attached_phase.status(maxage)[0] == status.BUSY):
            return status.BUSY, 'Phase moving to target'

        return status.OK, 'Main' if self.isMain else 'Subordinate'

    @property
    def isMain(self):
        return self._get_pv('state') == 0

    def doReadSpeed(self):
        return self._get_pv('speed')

    def doWriteSpeed(self, value):
        if self._attached_speed:
            if self.isMain:
                self._attached_speed.start(value)
            else:
                raise UsageError(
                    'A subordinate cannot set speed. Please ask my main')
        else:
            raise ConfigurationError('No device attached to set the speed')

    def doReadPhase(self):
        return self._get_pv('phase')

    def doWritePhase(self, value):
        if self._attached_phase:
            if not self.isMain:
                self._attached_phase.start(value)
            else:
                raise UsageError(
                    'I am a main, ask my subordinate to set its phase')
        else:
            raise ConfigurationError('No device attached to set the phase')

    def doReadRatio(self):
        return self._get_pv('ratio')

    def doWriteRatio(self, value):
        if self._attached_ratio:
            if not self.isMain:
                self._attached_ratio.start(value)
            else:
                raise UsageError(
                    'I am a main, ask my subordinate to set its ratio')
        else:
            raise ConfigurationError('No device attached to set the ratio')


class EpicsAstriumChopper(HasPrecision, Readable):
    """Main class to control Astrium Chopper in SINQ instruments. A list
    of attached choppers provide the chopper discs in the system.

    Speed for the whole system can be change using main speed
    value subordinate speed ratios. The phases for each subordinate can also
    be changed.
    """

    attached_devices = {
        'choppers': Attach('Chopper disks in the system', EpicsChopperDisc,
                           multiple=True)
    }

    parameter_overrides = {
        'unit': Override(mandatory=False, userparam=False),
        'fmtstr': Override(userparam=False),
        'maxage': Override(userparam=False),
        'pollinterval': Override(userparam=False),
        'warnlimits': Override(userparam=False)
    }

    _main = None

    def doInit(self, mode):
        if len(self._attached_choppers) == 1:
            self._main = self._attached_choppers[0]
            return

        for ch in self._attached_choppers:
            if ch.isMain:
                self._main = ch
                return

        if not self._main:
            raise ConfigurationError(
                'Did not find any main! Check the EPICS PV State.')

    def doRead(self, maxage=0):
        return ''

    def doStatus(self, maxage=0):
        errors = []

        # Check for errors
        for ch in self._attached_choppers:
            st = ch.status()
            if st[0] == status.ERROR:
                errors.append('ERROR on %s: %s' % (ch.name, st[1]))

        if errors:
            return status.ERROR, ', '.join(errors)

        # Check if phase for any subordinates is being set
        busy = []
        for ch in self._attached_choppers:
            st = ch.status()
            if ch is self._main:
                if st[0] == status.BUSY:
                    # If the main subordinate is busy, that means the speed
                    # is still moving to target
                    busy.append('Moving to target speed')
            elif (abs(ch.ratio * ch.speed - self._main.speed) >
                  self.precision):
                # If a subordinate speed ratio does not match with the main,
                # this would imply the speed of subordinate is being changed
                busy.append('Setting the correct speed of %s' % ch.name)
            elif st[0] == status.BUSY:
                # If the actual status of a subordinate is busy, this would
                # mean that the phase is changing for that subordinate
                busy.append('Setting the phase of %s' % ch.name)

        if busy:
            return status.BUSY, ', '.join(busy)

        return status.OK, 'Spinning' if self._main.speed > 0 else 'Idle'

    @requires(level=ADMIN)
    def main_speed(self, speed):
        """Change the speed of the main chopper
        :param speed: new speed of the main. In case there are subordinates, the
                      speed can be adjusted using the ratio variable
        """
        self._main.speed = speed

    @requires(level=ADMIN)
    def ch_phase(self, ch_name, phase):
        """Change the phase of given subordinate disc
        :param ch_name: name of the subordinate chopper disc
        :param phase: new phase value
        """
        if ch_name == self._main.name:
            raise UsageError("Can't set the phase for main")

        ch = [x for x in self._attached_choppers if x.name == ch_name]
        if not ch:
            raise UsageError("Didn't find the subordinate: %s" % ch_name)

        ch[0].phase = phase

    @requires(level=ADMIN)
    def ch_ratio(self, ch_name, ratio):
        """Change the speed ratio to main of the given subordinate
        :param ch_name: name of the subordinate chopper disc
        :param ratio: new ratio value
        """
        if ch_name == self._main.name:
            raise UsageError("Can't set the ratio for main")

        ch = [x for x in self._attached_choppers if x.name == ch_name]
        if not ch:
            raise UsageError("Didn't find the subordinate: %s" % ch_name)

        ch[0].ratio = ratio

    @requires(level=ADMIN)
    def maintain_speed(self):
        """Stops changing the speed of the chopper disks
        """
        self.main_speed(self._main.speed)
