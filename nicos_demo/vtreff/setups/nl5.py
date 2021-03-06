description = 'FRM II neutron guide line 5 shutter'

group = 'lowlevel'

includes = ['guidehall']


devices = dict(
    NL5 = device('nicos.devices.generic.ManualSwitch',
        description = 'NL5 shutter status',
        states = ('open', 'closed'),
        pollinterval = 60,
        maxage = 120,
    ),
)
