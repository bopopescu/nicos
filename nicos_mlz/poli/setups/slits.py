description = 'POLI slits'

group = 'lowlevel'

includes = ['mono']

tango_base = 'tango://phys.poli.frm2:10000/poli/'
s7_motor = tango_base + 's7_motor/'

devices = dict(
    bmv = device('nicos.devices.tango.Motor',
        description = 'Monochromator vertical opening slit',
        tangodevice = s7_motor + 'bmv',
        fmtstr = '%.2f',
        abslimits = (114.5, 188),
        precision = 0.2,
        lowlevel = False,
    ),
    bmh = device('nicos.devices.tango.Motor',
        description = 'Monochromator horizontal opening slit',
        tangodevice = s7_motor + 'bmh',
        fmtstr = '%.2f',
        abslimits = (6.5, 80),
        precision = 0.2,
        lowlevel = False,
    ),
    bm = device('nicos.devices.generic.TwoAxisSlit',
        description = 'Monochromator slit',
        pollinterval = 15,
        maxage = 61,
        fmtstr = '%.2f %.2f',
        horizontal = 'bmh',
        vertical = 'bmv',
    ),
    bpr = device('nicos.devices.tango.Motor',
        description = 'Aperture sample right',
        tangodevice = s7_motor + 'bpl',
        lowlevel = True,
        precision = 0.1,
    ),
    bpl = device('nicos.devices.tango.Motor',
        description = 'Aperture sample left',
        tangodevice = s7_motor + 'bpr',
        lowlevel = True,
        precision = 0.1,
    ),
    bpo = device('nicos.devices.tango.Motor',
        description = 'Aperture sample upper',
        tangodevice = s7_motor + 'bpo',
        lowlevel = True,
        precision = 0.1,
    ),
    bpu = device('nicos.devices.tango.Motor',
        description = 'Aperture sample lower',
        tangodevice = s7_motor + 'bpu',
        lowlevel = True,
        precision = 0.1,
    ),
    bp = device('nicos.devices.generic.Slit',
        description = 'Aperture before sample',
        left = 'bpl',
        right = 'bpr',
        bottom = 'bpu',
        top = 'bpo',
        pollinterval = 5,
        maxage = 10,
        coordinates = 'opposite',
        opmode = '4blades_opposite',
    ),

    bdl = device('nicos.devices.tango.Motor',
        description = 'Aperture detector left',
        tangodevice = s7_motor + 'bdl',
        lowlevel = True,
        precision = 0.1,
    ),
    bdr = device('nicos.devices.tango.Motor',
        description = 'Aperture detector right',
        tangodevice = s7_motor + 'bdr',
        lowlevel = True,
        precision = 0.1,
    ),
    bdo = device('nicos.devices.tango.Motor',
        description = 'Aperture detector upper',
        tangodevice = s7_motor + 'bdo',
        lowlevel = True,
        precision = 0.1,
    ),
    bdu = device('nicos.devices.tango.Motor',
        description = 'Aperture detector lower',
        tangodevice = s7_motor + 'bdu',
        lowlevel = True,
        precision = 0.1,
    ),
    bd = device('nicos.devices.generic.Slit',
        description = 'Aperture before detector',
        left = 'bdl',
        right = 'bdr',
        bottom = 'bdu',
        top = 'bdo',
        pollinterval = 5,
        maxage = 10,
        coordinates = 'opposite',
        opmode = '4blades_opposite',
    ),
)
