description = 'Neutron guide focussing devices'

group = 'lowlevel'

nethost = 'kompasshw.kompass.frm2'

devices = dict(
    lguide_m = device('devices.taco.Motor',
                      description = 'Long table motor',
                      tacodevice = '//%s/kompass/ltable/motor' % nethost,
                      abslimits = (-0.5, 209.5),
                      fmtstr = '%.2f',
                      lowlevel = True,
                     ),
    lguide_c = device('devices.taco.Coder',
                      description = 'Long table coder',
                      tacodevice = '//%s/kompass/ltable/coder' % nethost,
                      fmtstr = '%.2f',
                      lowlevel = True,
                     ),
    lguide = device('devices.generic.Axis',
                    description = 'Long table position',
                    motor = 'lguide_m',
                    coder = 'lguide_c',
                    fmtstr = '%.2f',
                    precision = 0.01,
                   ),
    sguide_m = device('devices.taco.Motor',
                      description = 'Short table motor',
                      tacodevice = '//%s/kompass/stable/motor' % nethost,
                      abslimits = (-0.5, 206.5),
                      fmtstr = '%.2f',
                      lowlevel = True,
                     ),
    sguide_c = device('devices.taco.Coder',
                      description = 'Short table coder',
                      tacodevice = '//%s/kompass/stable/coder' % nethost,
                      fmtstr = '%.2f',
                      lowlevel = True,
                     ),
    sguide = device('devices.generic.Axis',
                    description = 'Short table position',
                    motor = 'sguide_m',
                    coder = 'sguide_c',
                    fmtstr = '%.2f',
                    precision = 0.02,
                   ),
    guide = device('devices.generic.MultiSwitcher',
                   description = 'Neutron guide selector',
                   moveables = ['sguide', 'lguide'],
                   mapping = {'straight': [205.037, 208.8216],
                              'focussing': [0., 0.],
                              },
                   fallback = 'undefined',
                   fmtstr = '%s',
                   precision = [0.05, 0.05],
                   blockingmove = False,
                   lowlevel = False,
                   unit = '',
                  ),
)