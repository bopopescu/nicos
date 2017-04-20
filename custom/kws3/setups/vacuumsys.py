description = 'vacuum system monitoring'

group = 'lowlevel'

tango_base = 'tango://phys.kws3.frm2:10000/kws3/'

devices = dict(
    pi2_1 = device('devices.tango.Sensor',
                   description = 'pressure in selector',
                   tangodevice = tango_base + 'FZJDP_Analog/pi2_1',
                   unit = 'mbar',
                   fmtstr = '%.1e',
                   lowlevel = True,
                  ),

    pi2_2 = device('devices.tango.Sensor',
                   description = 'pressure in tube 1',
                   tangodevice = tango_base + 'FZJDP_Analog/pi2_2',
                   unit = 'mbar',
                   fmtstr = '%.1e',
                   lowlevel = True,
                  ),

    pi3_1 = device('devices.tango.Sensor',
                   description = 'pressure in mirror chamber',
                   tangodevice = tango_base + 'FZJDP_Analog/pi3_1',
                   unit = 'mbar',
                   fmtstr = '%.1e',
                   lowlevel = True,
                  ),

    pi1_1 = device('devices.tango.Sensor',
                   description = 'pressure in sample chamber 1',
                   tangodevice = tango_base + 'FZJDP_Analog/pi1_1',
                   unit = 'mbar',
                   fmtstr = '%.1e',
                   lowlevel = True,
                  ),

    pi2_4 = device('devices.tango.Sensor',
                   description = 'pressure in tube 2',
                   tangodevice = tango_base + 'FZJDP_Analog/pi2_4',
                   unit = 'mbar',
                   fmtstr = '%.1e',
                   lowlevel = True,
                  ),

    pi1_2 = device('devices.tango.Sensor',
                   description = 'pressure in sample chamber 2',
                   tangodevice = tango_base + 'FZJDP_Analog/pi1_2',
                   unit = 'mbar',
                   fmtstr = '%.1e',
                   lowlevel = True,
                  ),

    pi1_3 = device('devices.tango.Sensor',
                   description = 'pressure in tube 3',
                   tangodevice = tango_base + 'FZJDP_Analog/pi1_3',
                   unit = 'mbar',
                   fmtstr = '%.1e',
                   lowlevel = True,
                  ),
)