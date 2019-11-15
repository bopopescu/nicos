description = 'Slits'

group = 'lowlevel'

tango_base = 'tango://motorbox02.spodi.frm2.tum.de:10000/box/'
tango_base2 = 'tango://motorbox03.spodi.frm2.tum.de:10000/box/'

devices = dict(
    # Monochromator slit
    slitm_u = device('nicos.devices.generic.Axis',
        description = 'Monochromator slit upper blade',
        motor = 'slitm_u_m',
        coder = 'slitm_u_c',
        precision = 0.01,
    ),
    slitm_u_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base2 + 'slitm_u/motor',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slitm_u_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base2 + 'slitm_u/coder',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slitm_d = device('nicos.devices.generic.Axis',
        description = 'Monochromator slit lower blade',
        motor = 'slitm_d_m',
        coder = 'slitm_d_c',
        precision = 0.01,
    ),
    slitm_d_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base2 + 'slitm_d/motor',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slitm_d_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base2 + 'slitm_d/coder',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slitm_l = device('nicos.devices.generic.Axis',
        description = 'Monochromator slit left blade',
        motor = 'slitm_l_m',
        coder = 'slitm_l_c',
        precision = 0.01,
    ),
    slitm_l_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base2 + 'slitm_l/motor',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slitm_l_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base2 + 'slitm_l/coder',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slitm_r = device('nicos.devices.generic.Axis',
        description = 'Monochromator slit right blade',
        motor = 'slitm_r_m',
        coder = 'slitm_r_c',
        precision = 0.01,
    ),
    slitm_r_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base2 + 'slitm_r/motor',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slitm_r_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base2 + 'slitm_r/coder',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slitm = device('nicos_mlz.stressi.devices.slit.Slit',
        description = 'Monochromator slit 4 blades',
        left = 'slits_l',
        right = 'slits_r',
        bottom = 'slits_d',
        top = 'slits_u',
        coordinates = 'opposite',
        opmode = 'centered',
    ),
    slits_u = device('nicos.devices.tango.Motor',
        description = 'Sample slit upper blade',
        tangodevice = tango_base + 'slits_u/motor',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slits_d = device('nicos.devices.tango.Motor',
        description = 'Sample slit lower blade',
        tangodevice = tango_base + 'slits_d/motor',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slits_l = device('nicos.devices.tango.Motor',
        description = 'Sample slit left blade',
        tangodevice = tango_base + 'slits_l/motor',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    slits_r = device('nicos.devices.tango.Motor',
        description = 'Sample slit right blade',
        fmtstr = '%.2f',
        tangodevice = tango_base + 'slits_r/motor',
        lowlevel = True,
    ),
    slits = device('nicos.devices.generic.Slit',
        description = 'Sample slit 4 blades',
        left = 'slits_l',
        right = 'slits_r',
        bottom = 'slits_d',
        top = 'slits_u',
        coordinates = 'opposite',
        opmode = 'centered',
        parallel_ref = True,
    ),
)
