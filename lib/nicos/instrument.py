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

"""
NICOS Instrument device.
"""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"


from nicos.device import Device, Measurable, Param
from nicos.errors import UsageError


class Instrument(Device):
    """A special singleton device to represent the instrument."""

    parameters = {
        'instrument': Param('Instrument name', type=str, category='experiment'),
        'responsible': Param('Instrument responsible name and email',
                             type=str, category='experiment'),
    }

    attached_devices = {
        'detectors': [Measurable],
    }

    def doInit(self):
        self._detlist = None

    @property
    def detectors(self):
        if self._detlist is None:
            return self._adevs['detectors']
        return self._detlist

    def setDetectors(self, detlist):
        for det in detlist:
            if not isinstance(det, Measurable):
                raise UsageError(self, 'cannot use device %r as a detector: '
                                 'it is not a Measurable' % det)
        self._detlist = list(detlist)
