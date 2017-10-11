#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2017 by the NICOS contributors (see AUTHORS)
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
#   Jens Krüger <jens.krueger@frm2.tum.de>
#
# *****************************************************************************

"""NICOS pulse device test suite."""

from test.utils import raises

from nicos.core import ConfigurationError, status

session_setup = 'pulse'


def test_params(session):
    pulse1 = session.getDevice('pulse1')
    # check well defined device
    assert pulse1.onvalue == 'up'
    assert pulse1.offvalue == 'down'
    assert pulse1.ontime == 0.2

    # check the test for 'up' and 'down' values
    assert raises(ConfigurationError, session.getDevice, 'pulse2')
    assert raises(ConfigurationError, session.getDevice, 'pulse3')


def test_movement(session):
    pulse1 = session.getDevice('pulse1')
    sw = session.getDevice('sw')
    # check sequence running
    pulse1.maw('up')
    assert sw.read(0) == 'down'
    pulse1.maw('down')
    assert sw.read(0) == 'down'

    # read the used device which should have the onvalue after the half ontime
    pulse1.move('up')
    session.delay(pulse1.ontime / 2.)
    assert sw.read(0) == pulse1.onvalue
    pulse1.wait()
    assert sw.read(0) == pulse1.offvalue


def test_starting(session):
    pulse1 = session.getDevice('pulse1')
    # Test the start if sequence was running
    pulse1.move('up')
    assert pulse1.status(0)[0] == status.BUSY
    pulse1.maw('up')

    # Test the start if target == read value
    pulse1.maw('down')
    pulse1.move('down')