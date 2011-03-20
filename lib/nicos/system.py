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
NICOS system device.
"""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"

from nicos import session
from nicos.data import DataSink
from nicos.device import Device
from nicos.notify import Notifier
from nicos.instrument import Instrument
from nicos.experiment import Experiment
from nicos.cache.client import CacheClient


class System(Device):
    """A special singleton device that serves for global configuration of
    the NICOS system.  It is not intended to be used directly, but via the
    session's properties and methods.
    """

    attached_devices = {
        'cache': CacheClient,
        'datasinks': [DataSink],
        'instrument': Instrument,
        'experiment': Experiment,
        'notifiers': [Notifier],
    }

    def __repr__(self):
        return '<NICOS System>'
