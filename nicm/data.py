#  -*- coding: utf-8 -*-
# *****************************************************************************
# Module:
#   $Id$
#
# Description:
#   Data handling classes for NICOS
#
# Author:
#   Georg Brandl <georg.brandl@frm2.tum.de>
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

"""Data handling classes for NICOS."""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"

import time
from os import path

from nicm import nicos
from nicm.utils import listof
from nicm.device import Device, Param
from nicm.commands.output import printinfo


TIMEFMT = '%Y-%m-%d %H:%M:%S'


class DataSink(Device):
    """
    A DataSink is a configurable object that receives measurement data.  All
    data handling is done by sinks; e.g. displaying it on the console or saving
    to a data file.
    """

    parameters = {
        'scantypes': Param('Scan types for which the sink is active',
                           type=listof(str), default=[]),
    }

    # Set to false in subclasses that e.g. write to the filesystem.
    activeInSimulation = True

    def prepareDataset(self):
        """Prepare for a new dataset.

        Returns a list of info about the new dataset as ``(key, value)`` pairs.
        A list of all these pairs is then passed to all sinks' `beginDataset()`
        as the *sinkinfo* parameter.  This is meant for sinks that write files
        to communicate the file name to sinks that write the info to the console
        or display them otherwise.
        """
        return []

    def beginDataset(self, devices, positions, detlist, preset,
                     userinfo, sinkinfo):
        """Begin a new dataset.

        The dataset will contain x-values for all *devices* (a list of `Device`
        objects), measured at *positions* (a list of lists, or None if the
        positions are not yet known).

        The dataset will contain y-values measured by the *detlist* using the
        given *preset* (a dictionary).

        *userinfo* is an arbitrary string.  *sinkinfo* is a list of ``(key,
        value)`` pairs as explained in `prepareDataset()`.
        """
        pass

    def addInfo(self, category, valuelist):
        """Add additional information to the dataset.

        This is meant to record e.g. device values at scan startup.  *valuelist*
        is a sequence of tuples ``(device, key, value)``.
        """
        pass

    def addPoint(self, num, xvalues, yvalues):
        """Add a point to the dataset.

        *num* is the number of the point in the scan
        *xvalues* is a list of values with the same length as the initial
        *devices* list given to `beginDataset()`, and *yvalues* is a list of
        values with the same length as the all of detlist's value lists.
        """
        pass

    def endDataset(self):
        """End the current dataset."""
        pass

    def setDatapath(self, value):
        # XXX needed?
        pass


class ConsoleSink(DataSink):

    def beginDataset(self, devices, positions, detlist, preset,
                     userinfo, sinkinfo):
        printinfo('=' * 80)
        printinfo('Starting scan:      ' + (userinfo or ''))
        for name, value in sinkinfo:
            printinfo('%-20s%s' % (name+':', value))
        printinfo('Started at:         ' + time.strftime(TIMEFMT))
        printinfo('-' * 80)
        detnames = []
        detunits = []
        for det in detlist:
            names, units = det.valueInfo()
            detnames.extend(names)
            detunits.extend(units)
        printinfo('\t'.join(map(str, ['#'] + devices + detnames))
                  .expandtabs())
        printinfo('\t'.join([''] + [dev.unit for dev in devices] +
                            detunits).expandtabs())
        printinfo('-' * 80)
        if positions:
            self._npoints = len(positions)
        else:
            self._npoints = 0

    def addPoint(self, num, xvalues, yvalues):
        if self._npoints:
            point = '%s/%s' % (num, self._npoints)
        else:
            point = num
        printinfo('\t'.join(map(str, [point] + xvalues + yvalues))
                  .expandtabs())

    def endDataset(self):
        printinfo('-' * 80)
        printinfo('Finished at:        ' + time.strftime(TIMEFMT))
        printinfo('=' * 80)


class DatafileSink(DataSink):

    activeInSimulation = False



class AsciiDatafileSink(DatafileSink):
    parameters = {
        # XXX prefix should come from proposal
        'prefix': Param('Data file name prefix', type=str),
        'semicolon': Param('Whether to add a semicolon between X and Y values',
                           type=bool, default=True),
    }

    def doInit(self):
        self._path = None
        self._file = None
        self._fname = ''
        self._counter = 0

    def doWritePrefix(self, value):
        if value and not value.endswith('_'):
            value += '_'
        return value

    def setDatapath(self, value):
        self._path = value
        self._counter = 0  # XXX determine current counter

    def prepareDataset(self):
        if self._path is None:
            self.setDatapath(nicos.system.datapath)
        self._wrote_columninfo = False
        self._counter += 1
        self._fname = path.join(self._path, self.prefix +
                                '%s.dat' % self._counter)
        return [('File name', self._fname)]

    def beginDataset(self, devices, positions, detlist, preset,
                     userinfo, sinkinfo):
        self._file = open(self._fname, 'w')
        self._userinfo = userinfo
        self._file.write('### NICOS data file, created at %s\n' %
                         time.strftime(TIMEFMT))
        for name, value in sinkinfo:
            self._file.write('# %-25s%s\n' % (name+':', value))
        self._file.write('# Info:                    %s\n' % userinfo)
        self._file.flush()
        # to be written later (after info)
        devnames = map(str, devices)
        devunits = [dev.unit for dev in devices]
        detnames = []
        detunits = []
        for det in detlist:
            names, units = det.valueInfo()
            detnames.extend(names)
            detunits.extend(units)
        if self.semicolon:
            self._colnames = devnames + [';'] + detnames
            self._colunits = devunits + [';'] + detunits
        else:
            self._colnames = devnames + detnames
            self._colunits = devunits + detunits

    def addInfo(self, category, valuelist):
        self._file.write('### %s\n' % category)
        for device, key, value in valuelist:
            self._file.write('# %25s : %s\n' % (device.name + '_' + key, value))
        self._file.flush()

    def addPoint(self, num, xvalues, yvalues):
        if not self._wrote_columninfo:
            self._file.write('### Measurement data\n')
            self._file.write('# ' + '\t'.join(self._colnames) + '\n')
            self._file.write('# ' + '\t'.join(self._colunits) + '\n')
            self._wrote_columninfo = True
        if self.semicolon:
            values = xvalues + [';'] + yvalues
        else:
            values = xvalues + yvalues
        self._file.write('\t'.join(map(str, values)) + '\n')
        self._file.flush()

    def endDataset(self):
        self._file.write('### End of NICOS data file %s\n' % self._fname)
        self._file.close()
        self._file = None
