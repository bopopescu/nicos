description = 'HUBER Sample Table Experimental Chamber 1'

group = 'optional'

tango_base = 'tango://slow.antares.frm2:10000/antares/'

devices = dict(
    stx_huber = device('devices.tango.Motor',
                       description = 'Sample Translation X',
                       tangodevice = tango_base + 'fzjs7/Probe_X',
                       precision = 0.01,
                       abslimits = (0, 400),
                       pollinterval = 5,
                       maxage = 12,
                      ),
    sty_huber = device('devices.tango.Motor',
                       description = 'Sample Translation Y',
                       tangodevice = tango_base + 'fzjs7/Probe_Y',
                       precision = 0.01,
                       abslimits = (0, 400),
                       pollinterval = 5,
                       maxage = 12,
                      ),
    sgx_huber       = device('devices.tango.Motor',
                       description = 'Sample Rotation around X',
                       tangodevice = tango_base + 'fzjs7/Probe_tilt_x',
                       precision = 0.01,
                       abslimits = (-10, 10),
                       pollinterval = 5,
                       maxage = 12,
                      ),
    sgz_huber       = device('devices.tango.Motor',
                       description = 'Sample Rotation around Z',
                       tangodevice = tango_base + 'fzjs7/Probe_tilt_z',
                       precision = 0.01,
                       abslimits = (-10, 10),
                       pollinterval = 5,
                       maxage = 12,
                      ),
    sry_huber = device('devices.tango.Motor',
                       description = 'Sample Rotation around Y',
                       tangodevice = tango_base + 'fzjs7/Probe_phi',
                       precision = 0.01,
                       abslimits = (-999999, 999999),
                       pollinterval = 5,
                       maxage = 12,
                      ),
)

startupcode = '''
'''
