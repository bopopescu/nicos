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

name = 'test_toftof setup'

includes = ['stdsystem']

sysconfig = dict(
    datasinks = ['tofsink'],
)

devices = dict(
    monitor = device('devices.generic.VirtualCounter',
        type = 'monitor',
    ),
    timer = device('devices.generic.VirtualTimer',
        unit = 's',
    ),
    image = device('toftof.virtual.VirtualImage',
        pollinterval = 86400,
        datafile = 'custom/toftof/data/test/data.npz',
    ),
    det = device('toftof.detector.Detector',
        timers = ['timer'],
        monitors = ['monitor'],
        counters = [],
        images = ['image'],
        rc = 'rc',
        chopper = 'ch',
        chdelay = 'chdelay',
        maxage = 3,
        pollinterval = None,
        liveinterval = 0.5,
        saveintervals = [0.5],
        detinfofile = 'custom/toftof/detinfo.dat',
    ),
    d1 = device('toftof.chopper.Disc',
        speed = 0,
        jitter = 0,
    ),
    d2 = device('toftof.chopper.Disc',
        speed = 0,
        jitter = 0,
    ),
    d3 = device('toftof.chopper.Disc',
        speed = 0,
        jitter = 0,
    ),
    d4 = device('toftof.chopper.Disc',
        speed = 0,
        jitter = 0,
    ),
    d5 = device('toftof.chopper.Disc',
        speed = 0,
        jitter = 0,
    ),
    d6 = device('toftof.chopper.Disc',
        speed = 0,
        jitter = 0,
    ),
    d7 = device('toftof.chopper.Disc',
        speed = 0,
        jitter = 0,
    ),
    ch = device('toftof.chopper.VirtualController',
        speed_accuracy = 40,
        phase_accuracy = 10,
        ch5_90deg_offset = 0,
        timeout = 600,
        unit = 'rpm',
        discs = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7'],
        # abslimits = (0., 27000),
    ),
    chSpeed = device('toftof.chopper.Speed',
        chopper = 'ch',
        chdelay = 'chdelay',
        abslimits = (0, 22000.),
        unit = 'rpm',
    ),
    chDS = device('toftof.chopper.SpeedReadout',
        chopper = 'ch',
        unit = 'rpm',
    ),
    chWL = device('toftof.chopper.Wavelength',
        chopper = 'ch',
        chdelay = 'chdelay',
        abslimits = (0.2, 16.0),
        unit = 'AA',
    ),
    chRatio = device('toftof.chopper.Ratio',
        chopper = 'ch',
        chdelay = 'chdelay',
    ),
    chCRC = device('toftof.chopper.CRC',
        chopper = 'ch',
        chdelay = 'chdelay',
    ),
    chST = device('toftof.chopper.SlitType',
        chopper = 'ch',
        chdelay = 'chdelay',
    ),
    chdelay = device('devices.generic.ManualMove',
        abslimits = (0, 1000000),
        unit = 'usec',
    ),
    gx = device('devices.generic.VirtualMotor',
        abslimits = (-20.0, 20.),
        unit = 'mm',
    ),
    gy = device('devices.generic.VirtualMotor',
        abslimits = (-20.0, 20.),
        unit = 'mm',
    ),
    gz = device('devices.generic.VirtualMotor',
        abslimits = (-14.8, 50.),
        unit = 'mm',
    ),
    gcx = device('devices.generic.VirtualMotor',
        abslimits = (-20.0, 20.),
        unit = 'deg',
    ),
    gcy = device('devices.generic.VirtualMotor',
        abslimits = (-20.0, 20.),
        unit = 'deg',
    ),
    gphi = device('devices.generic.VirtualMotor',
        abslimits = (-20.0, 150.),
        unit = 'deg',
    ),
    slit = device('devices.generic.Slit',
        bottom = device('devices.generic.VirtualMotor',
            abslimits = (-200, 46.425),
            unit = 'mm',
        ),
        top = device('devices.generic.VirtualMotor',
            abslimits = (-200, 46.425),
            unit = 'mm',
        ),
        left = device('devices.generic.VirtualMotor',
            abslimits = (-200, 27.5),
            unit = 'mm',
        ),
        right = device('devices.generic.virtual.VirtualMotor',
            abslimits = (-200, 27.5),
            unit = 'mm',
        ),
        coordinates = 'opposite',
        opmode = 'offcentered',
    ),
    hv0 = device('devices.generic.VirtualMotor',
        abslimits = (0, 1600),
        ramp = 0,
        unit = 'V',
    ),
    hv1 = device('devices.generic.VirtualMotor',
        abslimits = (0, 1600),
        ramp = 0,
        unit = 'V',
    ),
    hv2 = device('devices.generic.VirtualMotor',
        abslimits = (0, 1600),
        ramp = 0,
        unit = 'V',
    ),
    lv0 = device('devices.generic.ManualSwitch',
        states = ['off', 'on']
    ),
    lv1 = device('devices.generic.ManualSwitch',
        states = ['off', 'on']
    ),
    lv2 = device('devices.generic.ManualSwitch',
        states = ['off', 'on']
    ),
    lv3 = device('devices.generic.ManualSwitch',
        states = ['off', 'on']
    ),
    lv4 = device('devices.generic.ManualSwitch',
        states = ['off', 'on']
    ),
    lv5 = device('devices.generic.ManualSwitch',
        states = ['off', 'on']
    ),
    lv6 = device('devices.generic.ManualSwitch',
        states = ['off', 'on']
    ),
    lv7 = device('devices.generic.ManualSwitch',
        states = ['off', 'on']
    ),
    vac0 = device('devices.generic.ManualMove',
        default = 1.7e-6,
        abslimits = (0, 1000),
        unit = 'mbar',
    ),
    vac1 = device('devices.generic.ManualMove',
        default = 0.00012,
        abslimits = (0, 1000),
        unit = 'mbar',
    ),
    vac2 = device('devices.generic.ManualMove',
        default = 3.5e-6,
        abslimits = (0, 1000),
        unit = 'mbar',
    ),
    vac3 = device('devices.generic.ManualMove',
        default = 5.0e-6,
        abslimits = (0, 1000),
        unit = 'mbar',
    ),
    ngc = device('toftof.neutronguide.Switcher',
        moveable = device('devices.generic.VirtualMotor',
            userlimits = (-131.4, 0.),
            abslimits = (-131.4, 0.),
            unit = 'mm',
        ),
        mapping = {
            'linear': -5.1,
            'focus': -131.25,
        },
    ),
    rc = device('devices.generic.ManualSwitch',
        states = ['off', 'on'],
    ),
    B = device('devices.generic.VirtualMotor',
        abslimits = (0, 1),
        unit = 'T',
    ),
    P = device('devices.generic.VirtualMotor',
        abslimits = (0, 1000),
        unit = 'mbar',
    ),
    T = device('devices.generic.VirtualMotor',
        abslimits = (-40, 100),
        unit = 'degC',
    ),
    tofsink = device('toftof.datasinks.TofImageSink',
        filenametemplate = ['%(pointcounter)08d_0000.raw'],
    ),
)