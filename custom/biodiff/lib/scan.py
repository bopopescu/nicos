# -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
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

from __future__ import print_function

# standard library
import math
# local library
from nicos import session
from nicos.core import Moveable, UsageError
from nicos.core.scan import Scan
from nicos.core.spm import spmsyntax, Dev, Bare
from nicos.commands import usercommand, helparglist
from nicos.commands.scan import _handleScanArgs, _infostr


__author__ = "Christian Felder <c.felder@fz-juelich.de>"
__date__ = "2014-06-03"
__version__ = "0.1.0"


class RScan(Scan):

    def preparePoint(self, num, xvalues):
        if num > 0: # skip starting point, because of range scan (0..1, ...)
            Scan.preparePoint(self, num, xvalues)
        else:
            if self.dataset.npoints == 0:
                session.beginActionScope('Point %d' % num)
            else:
                session.beginActionScope('Point %d/%d' % (num,
                                                          self.dataset.npoints))


def _fixType(dev, args, mkpos):
    if not args:
        raise UsageError('at least two arguments are required')
    if isinstance(dev, list):
        if not isinstance(args[0], list):
            raise UsageError('positions must be a list if devices are a list')
        devs = dev
        if isinstance(args[0][0], list):
            for l in args[0]:
                if len(l) != len(args[0][0]):
                    raise UsageError('all position lists must have the same '
                                     'number of entries')
            values = list(zip(*args[0]))
            restargs = args[1:]
        else:
            if len(args) < 3:
                raise UsageError('at least four arguments are required in '
                                 'start-step-end scan command')
            if not (isinstance(args[0], list) and isinstance(args[1], list)
                    and isinstance(args[2], list)):
                raise UsageError('start, step and end must be lists')
            if not len(dev) == len(args[0]) == len(args[1]) == len(args[2]):
                raise UsageError('start, step and end lists must be of ' +
                                 'equal length')
            values = mkpos(args[0], args[1], args[2])
            restargs = args[3:]
    else:
        devs = [dev]
        if isinstance(args[0], list):
            values = list(zip(args[0]))
            restargs = args[1:]
        else:
            if len(args) < 3:
                raise UsageError('at least four arguments are required in '
                                 'start-step-end scan command')
            values = mkpos([args[0]], [args[1]], [args[2]])
            restargs = args[3:]
    devs = [session.getDevice(d, Moveable) for d in devs]
    return devs, values, restargs

@usercommand
@helparglist('dev, [start, step, end | listofpoints], t=seconds, ...')
@spmsyntax(Dev(Moveable), Bare, Bare, Bare)
def rscan(dev, *args, **kwargs):
    """Scan ranges over device(s) and count detector(s).

    The general syntax is either to give start, step and end:

    >>> rscan(dev, 0, 1, 10)   # scans from 0 to 10 in steps of 1.

    or a list of positions to scan:

    >>> rscan(dev, [0, 1, 2, 3, 7, 8, 9, 10])  # scans at the given positions.

    """
    def mkpos(starts, steps, ends):
        def mk(starts, steps, numpoints):
            return [[start + i * step for (start, step) in zip(starts, steps)]
                    for i in range(int(numpoints))]
        numpoints = [(end - start) / step + 1
                     for (start, step, end) in zip(starts, steps, ends)]
        if all(n == numpoints[0] for n in numpoints):
            if numpoints[0] > 0:
                return mk(starts, steps, numpoints[0])
            else:
                raise UsageError("""negative number of points.
Please check parameters. Maybe step parameter has wrong sign.""")
        else:
            raise UsageError("all entries must generate the same " +
                             "number of points")

    scanstr = _infostr('rscan', (dev,) + args, kwargs)
    devs, values, restargs = _fixType(dev, args, mkpos)
    preset, scaninfo, detlist, envlist, move, multistep  = \
        _handleScanArgs(restargs, kwargs, scanstr)
    oldspeed = dev.speed
    if len(values) > 1:
        step = values[1][0] - values[0][0]
    if 't' in preset:
        speed = math.fabs(step / float(preset['t']))
        dev.speed = speed
    else:
        raise UsageError("missing preset parameter t.")
    RScan(devs, values, move, multistep, detlist, envlist, preset, scaninfo,
          waitbeforecount=False).run()
    dev.speed = oldspeed
