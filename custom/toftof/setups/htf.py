description = 'FRM-II high temperature furnace'

group = 'optional'

includes = ['system', 'alias_T']

nethost = 'toftofsrv.toftof.frm2'

devices = dict(
    oven = device('devices.taco.TemperatureController',
                  tacodevice = '//%s/toftof/htf/control' % (nethost, ),
                  userlimits = (0, 2000),
                  abslimits = (0, 2000),
                  ramp = 0.1,
                  unit = 'C',
                  fmtstr = '%.3f',
                 ),
)

startupcode = """
Ts.alias = oven
T.alias = oven
AddEnvironment(Ts, T)
"""
