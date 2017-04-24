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

name = 'test_refsans setup'

includes = ['detector']

sysconfig = dict(
    datasinks = ['configsink'],
)

devices = dict(
    nok1 = device('refsans.nok_support.SingleMotorNOK',
                  motor = device('devices.generic.VirtualMotor',
                                 unit = 'mm',
                                 abslimits = (-56.119, 1.381),
                                ),
                  nok_start = 198.0,
                  nok_length = 90.0,
                  nok_end = 288.0,
                  nok_gap = 1.0,
                  backlash = -2,
                  precision = 0.05,
                 ),
    nok2 = device('refsans.nok_support.DoubleMotorNOK',
                  nok_start = 334.0,
                  nok_length = 300.0,
                  nok_end = 634.0,
                  nok_gap = 1.0,
                  inclinationlimits = (-10, 10),
                  motor_r = device('devices.generic.Axis',
                                   motor = device('devices.generic.VirtualMotor',
                                                  unit = 'mm',
                                                  abslimits = (-25., 25.),
                                                 ),
                                   precision = 0.05,
                                  ),
                  motor_s = device('devices.generic.Axis',
                                   motor = device('devices.generic.VirtualMotor',
                                                  unit = 'mm',
                                                  abslimits = (-25., 25.),
                                                 ),
                                   precision = 0.05,
                                  ),
                  nok_motor = [408.5, 585.0],
                  backlash = -2,
                  precision = 0.05,
                 ),
    obs = device('refsans.nok_support.NOKPosition',
                 reference = device('devices.generic.VirtualCoder',
                                    motor = device('devices.generic.VirtualMotor',
                                                   abslimits = (0, 10),
                                                   unit = 'V',
                                                   curvalue = 10.,
                                                  ),
                                    unit = 'V',
                                   ),
                 measure = device('devices.generic.VirtualCoder',
                                  motor = device('devices.generic.VirtualMotor',
                                                 abslimits = (0, 10),
                                                 unit = 'V',
                                                 curvalue = 5.,
                                                ),
                                  unit = 'V',
                                 ),
                 # off, mul * 1000 / sensitivity, higher orders...
                 poly = [9., 900.],
                 serial = 6510,
                 length = 250.0,
                ),
    configsink = device('refsans.datasinks.ConfigObjDatafileSink',
                        lowlevel = True,
                       ),
    vacuum_CB = device('devices.generic.ManualMove',
                       default = 3.5e-6,
                       abslimits = (0, 1000),
                       unit = 'mbar',
                      ),
    shutter = device('devices.generic.ManualSwitch',
                     states = ['close', 'open'],
                    ),
    zb0 = device('refsans.nok_support.SingleMotorNOK',
                 motor = device('devices.generic.VirtualMotor',
                                abslimits = (-180.815, 69.185),
                                speed = 5,
                                unit = 'mm',
                               ),
                 obs = [],
                 nok_start = 4121.5,
                 nok_length = 13.0,
                 nok_end = 4134.5,
                 nok_gap = 1.0,
                 masks = dict(
                              k1 = [-110.0, 0.0],
                              slit = [0.0, 0.0],
                             ),
                 nok_motor = 4128.5,
                 backlash = -2,
                 precision = 0.05,
                ),
    table = device('devices.generic.Axis',
                   motor = device('devices.generic.VirtualMotor',
                                  abslimits = (620, 11025),
                                  unit = 'mm',
                                 ),
                   precision = 0.05,
                  ),
    tube = device('devices.generic.VirtualMotor',
                  description = 'tube Motor',
                  abslimits = (-120, 1000),
                  unit = 'mm',
                 ),
    h2_width = device('devices.generic.VirtualMotor',
                      unit = 'mm',
                      abslimits = (-69.5, 69.5),
                     ),
    h2_center = device('devices.generic.VirtualMotor',
                       unit = 'mm',
                       abslimits = (0.05, 69.5),
                      ),
    top_phi = device('devices.generic.VirtualMotor',
                     abslimits = (-10.5, 10.5),
                     unit = 'deg',
                    ),
    pivot = device('devices.generic.ManualSwitch',
                   states = list(range(1, 14)),
                  ),
)
