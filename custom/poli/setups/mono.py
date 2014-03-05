description = 'POLI monochromator'

group = 'lowlevel'

includes = []

nethost = 'slow.poli.frm2'

devices = dict(
    chi_m = device('devices.taco.Motor',
                   description = 'monochromator tilt (chi axis)',
                   tacodevice = '//%s/poli/fzjs7/chi_m' % (nethost, ),
                   pollinterval = 15,
                   maxage = 61,
                   fmtstr = '%.2f',
                   abslimits = (0, 10),
                  ),
    theta_m = device('devices.taco.Motor',
                     description = 'monochromator rotation (theta axis)',
                     tacodevice = '//%s/poli/fzjs7/theta_m' % (nethost, ),
                     pollinterval = 15,
                     maxage = 61,
                     fmtstr = '%.2f',
                     abslimits = (-1, 10),
                    ),
    x_m = device('devices.taco.Motor',
                 description = 'monochromator translation (x axis)',
                 tacodevice = '//%s/poli/fzjs7/x_m' % (nethost, ),
                 pollinterval = 15,
                 maxage = 61,
                 fmtstr = '%.2f',
                 abslimits = (0, 50),
                ),
    changer_m = device('devices.taco.Motor',
                       description = 'monochromator changer axis',
                       tacodevice = '//%s/poli/fzjs7/change_m' % (nethost, ),
                       pollinterval = 15,
                       maxage = 61,
                       fmtstr = '%.2f',
                       abslimits = (0, 180),
                      ),
)

startupcode = """
"""
