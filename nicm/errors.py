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

"""Exception classes for usage in NICOS."""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"


class NicmError(Exception):
    category = 'Error'
    device = None
    tacoerr = None

    def __init__(self, *args, **kwds):
        # store the originating device on the exception
        args = list(args)
        if args and not isinstance(args[0], basestring):
            self.device = args[0]
            args[0] = '[%s] ' % args[0].name
        self.__dict__.update(kwds)
        Exception.__init__(self, ''.join(args))


class ProgrammingError(NicmError):
    category = 'Programming error'

class ConfigurationError(NicmError):
    category = 'Configuration error'

class UsageError(NicmError):
    category = 'Usage error'

class ModeError(NicmError):
    category = 'Mode error'

class PositionError(NicmError):
    category = 'Position error'

class MoveError(NicmError):
    category = 'Positioning error'

class LimitError(NicmError):
    category = 'Out of bounds'

class FixedError(NicmError):
    category = 'Device fixed'

class CommunicationError(NicmError):
    category = 'Communication error'

class TimeoutError(CommunicationError):
    category = 'Timeout'

class ComputationError(NicmError):
    category = 'Computation error'

class CacheLockError(ProgrammingError):
    def __init__(self, locked_by):
        self.locked_by = locked_by
        ProgrammingError.__init__(self, 'locked by ' + locked_by)
