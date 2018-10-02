#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2018 by the NICOS contributors (see AUTHORS)
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

from __future__ import absolute_import

from os import path

from nicos import session
from nicos.core import SIMULATION, Override
from nicos.core.errors import ProgrammingError
from nicos.utils import readFileCounter, updateFileCounter

from nicos_ess.devices.datasinks.nexussink import NexusFileWriterSink, \
    NexusFileWriterSinkHandler


class SinqNexusFileSinkHandler(NexusFileWriterSinkHandler):
    """Use the SICS counter so that counter is synchronized in all
    user control software.
    """

    def _assignCounter(self):
        # Adapted from DataManager.assignCounter function
        if self.dataset.counter != 0:
            return

        exp = session.experiment
        if not path.isfile(path.join(exp.dataroot, exp.counterfile)):
            session.log.warning('creating new empty file counter file at %s',
                                path.join(exp.dataroot, exp.counterfile))

        if session.mode == SIMULATION:
            raise ProgrammingError('assignCounter should not be called in '
                                   'simulation mode')

        # Read the counter from SICS file
        counter = exp.sicscounter + 1

        # Keep track of which files we have already updated, since the proposal
        # and the sample specific counter might be the same file.
        seen = set()
        for directory, attr in [(exp.dataroot, 'counter'),
                                (exp.proposalpath, 'propcounter'),
                                (exp.samplepath, 'samplecounter')]:
            counterpath = path.normpath(path.join(directory, exp.counterfile))
            readFileCounter(counterpath, self.dataset.countertype)
            if counterpath not in seen:
                updateFileCounter(counterpath, self.dataset.countertype,
                                  counter)
                seen.add(counterpath)

            setattr(self.dataset, attr, counter)

        # Update the counter in SICS file
        exp.updateSicsCounterFile(counter)

        session.experiment._setROParam('lastpoint', self.dataset.counter)

    def prepare(self):
        self._assignCounter()
        NexusFileWriterSinkHandler.prepare(self)


class SinqNexusFileSink(NexusFileWriterSink):
    parameter_overrides = {
        'subdir': Override(volatile=True),
    }

    handlerclass = SinqNexusFileSinkHandler

    def doReadSubdir(self):
        counter = session.experiment.sicscounter
        return ('%3s' % int(counter / 1000)).replace(' ', '0')
