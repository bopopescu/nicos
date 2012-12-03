description = 'test triple-axis setup'
group = 'basic'

includes = ['system']

modules = ['nicos.commands.tas']

sysconfig = dict(
    instrument = 'tas',
)

devices = dict(
    tas      = device('devices.tas.TAS',
                      description = 'test triple-axis spectrometer',
                      instrument = 'VTAS',
                      responsible = 'R. Esponsible <responsible@frm2.tum.de>',
                      energytransferunit = 'meV',
                      scanconstant = 1.5,
                      scanmode = 'CKF',
                      scatteringsense = (1, -1, 1),
                      axiscoupling = False,
                      collimation = '60 30 30 60',
                      cell = 'Sample',
                      phi = 'phi',
                      psi = 'psi',
                      mono = 'mono',
                      ana = 'ana',
                      alpha = None),

    phi      = device('devices.generic.VirtualMotor',
                      abslimits = (-180, 180),
                      curvalue = -38.942,
                      unit = 'deg'),

    alpha    = device('devices.generic.VirtualMotor',
                      abslimits = (0, 50),
                      unit = 'deg'),

    psi      = device('devices.generic.VirtualMotor',
                      abslimits = (0, 360),
                      curvalue = 70.529,
                      unit = 'deg'),

    mono     = device('devices.tas.Monochromator',
                      unit = 'A-1',
                      dvalue = 3.355,
                      theta = 'mth',
                      twotheta = 'mtt',
                      focush = None,
                      focusv = None,
                      abslimits = (0, 10)),

    mth      = device('devices.generic.VirtualMotor',
                      unit = 'deg',
                      abslimits = (0, 90),
                      precision = 0.05,
                      curvalue = 38.628),

    mtt      = device('devices.generic.VirtualMotor',
                      unit = 'deg',
                      abslimits = (0, 180),
                      precision = 0.05,
                      curvalue = 77.256),

    ana      = device('devices.tas.Monochromator',
                      unit = 'A-1',
                      dvalue = 3.355,
                      theta = 'ath',
                      twotheta = 'att',
                      focush = None,
                      focusv = None,
                      abslimits = (0, 10)),

    ath      = device('devices.generic.VirtualMotor',
                      unit = 'deg',
                      abslimits = (-90, 90),
                      precision = 0.05,
                      curvalue = 38.628),

    att      = device('devices.generic.VirtualMotor',
                      unit = 'deg',
                      abslimits = (-180, 180),
                      precision = 0.05,
                      curvalue = 77.256),

    ki       = device('devices.tas.Wavevector',
                      unit = 'A-1',
                      base = 'mono',
                      tas = 'tas',
                      scanmode = 'CKI',
                      abslimits = (0, 10)),

    kf       = device('devices.tas.Wavevector',
                      unit = 'A-1',
                      base = 'ana',
                      tas = 'tas',
                      scanmode = 'CKF',
                      abslimits = (0, 10)),

    ssl      = device('devices.generic.VirtualMotor',
                      abslimits = (-20, 40),
                      lowlevel = True,
                      unit = 'mm'),
    ssr      = device('devices.generic.VirtualMotor',
                      abslimits = (-40, 20),
                      lowlevel = True,
                      unit = 'mm'),
    ssb      = device('devices.generic.VirtualMotor',
                      abslimits = (-50, 30),
                      lowlevel = True,
                      unit = 'mm'),
    sst      = device('devices.generic.VirtualMotor',
                      abslimits = (-30, 50),
                      lowlevel = True,
                      unit = 'mm'),
    ss       = device('devices.generic.Slit',
                      left = 'ssl',
                      right = 'ssr',
                      bottom = 'ssb',
                      top = 'sst',
                      opmode = 'offcentered'),
)
