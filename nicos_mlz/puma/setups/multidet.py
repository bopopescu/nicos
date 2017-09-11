#  -*- coding: utf-8 -*-

description = 'Multidetector motors'

includes = ['system', 'motorbus10']

excludes = ['detectorM']

group = 'lowlevel'

devices = dict(
# Detectors
    st_rd11 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 71,
        slope = 4061.72,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd10 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 73,
        slope = 4709.53,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd9 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 75,
        slope = 4061.72,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd8 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 77,
        slope = 4709.53,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd7 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 79,
        slope = 4061.72,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd6 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 81,
        slope = 4709.53,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd5 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 83,
        slope = 4061.72,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd4 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 85,
        slope = 4709.53,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd3 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 87,
        slope = 4709.53,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd2 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 89,
        slope = 4061.72,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rd1 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 91,
        slope = 4709.53,
        unit = 'deg',
        abslimits = (-90, 5),
        zerosteps = 500000,
        lowlevel = True,
    ),
    rd11 = device('nicos.devices.generic.Axis',
        description = 'Detector 11 position',
        motor = 'st_rd11',
        obs = [],
        precision = 0.01,
        offset = 38.611,
        maxtries = 1,
    ),
    rd10 = device('nicos.devices.generic.Axis',
        description = 'Detector 10 position',
        motor = 'st_rd10',
        obs = [],
        precision = 0.01,
        offset = 36.198,
        maxtries = 1,
    ),
    rd9 = device('nicos.devices.generic.Axis',
        description = 'Detector 9 position',
        motor = 'st_rd9',
        obs = [],
        precision = 0.01,
        offset = 33.722,
        maxtries = 1,
    ),
    rd8 = device('nicos.devices.generic.Axis',
        description = 'Detector 8 position',
        motor = 'st_rd8',
        obs = [],
        precision = 0.01,
        offset = 31.257,
        maxtries = 1,
    ),
    rd7 = device('nicos.devices.generic.Axis',
        description = 'Detector 7 position',
        motor = 'st_rd7',
        obs = [],
        precision = 0.01,
        offset = 28.892,
        maxtries = 1,
    ),
    rd6 = device('nicos.devices.generic.Axis',
        description = 'Detector 6 position',
        motor = 'st_rd6',
        obs = [],
        precision = 0.01,
        offset = 26.499,
        maxtries = 1,
    ),
    rd5 = device('nicos.devices.generic.Axis',
        description = 'Detector 5 position',
        motor = 'st_rd5',
        obs = [],
        precision = 0.01,
        offset = 24.042,
        maxtries = 1,
    ),
    rd4 = device('nicos.devices.generic.Axis',
        description = 'Detector 4 position',
        motor = 'st_rd4',
        obs = [],
        precision = 0.01,
        offset = 21.652,
        maxtries = 1,
    ),
    rd3 = device('nicos.devices.generic.Axis',
        description = 'Detector 3 position',
        motor = 'st_rd3',
        obs = [],
        precision = 0.01,
        offset = 19.164,
        maxtries = 1,
    ),
    rd2 = device('nicos.devices.generic.Axis',
        description = 'Detector 2 position',
        motor = 'st_rd2',
        obs = [],
        precision = 0.01,
        offset = 16.857,
        maxtries = 1,
    ),
    rd1 = device('nicos.devices.generic.Axis',
        description = 'Detector 1 position',
        motor = 'st_rd1',
        obs = [],
        precision = 0.01,
        offset = 14.372,
        maxtries = 1,
    ),

# Guides
    st_rg11 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 72,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg10 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 74,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg9 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 76,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg8 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 78,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg7 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 80,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg6 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 82,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg5 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 84,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg4 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 86,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg3 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 88,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg2 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 90,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    st_rg1 = device('nicos.devices.vendor.ipc.Motor',
        bus = 'motorbus10',
        addr = 92,
        slope = -948,
        unit = 'deg',
        abslimits = (-50, 50),
        zerosteps = 500000,
        lowlevel = True,
    ),
    rg11 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 11 guide',
        motor = 'st_rg11',
        obs = [],
        precision = 0.01,
        offset = 7.27,
        maxtries = 1,
    ),
    rg10 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 10 guide',
        motor = 'st_rg10',
        obs = [],
        precision = 0.01,
        offset = 7.24,
        maxtries = 1,
    ),
    rg9 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 9 guide',
        motor = 'st_rg9',
        obs = [],
        precision = 0.01,
        offset = 7.13,
        maxtries = 1,
    ),
    rg8 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 8 guide',
        motor = 'st_rg8',
        obs = [],
        precision = 0.01,
        offset = 7.11,
        maxtries = 1,
    ),
    rg7 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 7 guide',
        motor = 'st_rg7',
        obs = [],
        precision = 0.01,
        offset = 7.34,
        maxtries = 1,
    ),
    rg6 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 6 guide',
        motor = 'st_rg6',
        obs = [],
        precision = 0.01,
        offset = 7.22,
        maxtries = 1,
    ),
    rg5 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 5 guide',
        motor = 'st_rg5',
        obs = [],
        precision = 0.01,
        offset = 7.41,
        maxtries = 1,
    ),
    rg4 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 4 guide',
        motor = 'st_rg4',
        obs = [],
        precision = 0.01,
        offset = 7.02,
        maxtries = 1,
    ),
    rg3 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 3 guide',
        motor = 'st_rg3',
        obs = [],
        precision = 0.01,
        offset = 7.04,
        maxtries = 1,
    ),
    rg2 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 2 guide',
        motor = 'st_rg2',
        obs = [],
        precision = 0.01,
        offset = 7.27,
        maxtries = 1,
    ),
    rg1 = device('nicos.devices.generic.Axis',
        description = 'Rotation of the detector 1 guide',
        motor = 'st_rg1',
        obs = [],
        precision = 0.01,
        offset = 7.73,
        maxtries = 1,
    ),
    med = device('nicos_mlz.puma.devices.multidetector.PumaMultiDetectorLayout',
        description = 'PUMA multi detector',
        rotdetector = ['rd1', 'rd2', 'rd3', 'rd4', 'rd5', 'rd6', 'rd7', 'rd8',
                       'rd9', 'rd10', 'rd11'],
        rotguide = ['rg1', 'rg2', 'rg3', 'rg4', 'rg5', 'rg6', 'rg7', 'rg8',
                    'rg9', 'rg10', 'rg11'],
        att = 'att',
    ),
    timer = device('nicos.devices.taco.FRMTimerChannel',
        description = 'QMesyDAQ timer',
        tacodevice = 'puma/qmesydaq/timer',
        lowlevel = True,
    ),
    mon1 = device('nicos.devices.taco.FRMCounterChannel',
        description = 'QMesyDAQ monitor 1',
        tacodevice = 'puma/qmesydaq/counter0',
        type = 'monitor',
        lowlevel = True,
        fmtstr = '%d',
    ),
    events = device('nicos.devices.vendor.qmesydaq.taco.Counter',
        description = 'QMesyDAQ Events channel',
        tacodevice = 'puma/qmesydaq/events',
        type = 'counter',
        lowlevel = True,
        fmtstr = '%d',
    ),
    image = device('nicos.devices.vendor.qmesydaq.taco.Image',
        description = 'QMesyDAQ Image',
        tacodevice = 'puma/qmesydaq/det',
        lowlevel = True,
    ),
    multidet = device('nicos.devices.generic.Detector',
        description = 'Puma detector QMesydaq device (3 counters)',
        timers = ['timer'],
        monitors = ['mon1'],
        images = ['image'],
        counters = [],
        maxage = 86400,
        pollinterval = None,
    ),
)