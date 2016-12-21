description = '(MC 2)'

group = 'optional'

tango_base = 'tango://phys.treff.frm2:10000/treff/'
tango_s7 = tango_base + 'FZJS7/'
taco_base = '//phys.treff.frm2/treff/'

excludes = ['virtual_mc2']

devices = dict(
    mc2_rot         = device('devices.tango.Motor',
                             description = 'MC2 rotation motor',
                             tangodevice = tango_s7 + 'mc2_rot',
                             precision = 0.01,
                             unit = 'deg',
                            ),
    mc2_x           = device('devices.tango.Motor',
                             description = 'MC2 x motor',
                             tangodevice = tango_s7 + 'mc2_x',
                             precision = 0.01,
                             unit ='mm',
                            ),
    mc2bus1         = device('treff.ipc.IPCModBusTacoJPB',
                             tacodevice = taco_base + 'goett/520',
                             lowlevel = True,
                            ),
    mc2_tilt_pg_mot = device('devices.vendor.ipc.Motor',
                             description = 'MC2 tilt PG motor',
                             bus = 'mc2bus1',
                             addr = 0,
                             abslimits = (-15.0, 15.0),
                             slope = -15300.0,
                             zerosteps = 500000,
                             speed = 150,
                             lowlevel = True,
                            ),
    mc2_tilt_pg     = device('devices.generic.Axis',
                             description = 'MC2 tilt PG',
                             motor = ' mc2_tilt_pg_mot',
                             coder = ' mc2_tilt_pg_mot',
                             precision = 0.01,
                             backlash = 0.07,
                             unit = 'deg',
                            ),
    mc2bus2         = device('treff.ipc.IPCModBusTacoJPB',
                             tacodevice = taco_base + 'goett/530',
                             lowlevel = True,
                            ),
    mc2_tilt_nb_mot = device('devices.vendor.ipc.Motor',
                             description = 'MC2 tilt NB motor',
                             bus = 'mc2bus2',
                             addr = 0,
                             abslimits = (-15.0, 15.0),
                             slope = 15300.0,
                             zerosteps = 500000,
                             speed = 150,
                             lowlevel = True,
                            ),
    mc2_tilt_nb     = device('devices.generic.Axis',
                             description = 'MC2 tilt PG',
                             motor = ' mc2_tilt_nb_mot',
                             coder = ' mc2_tilt_nb_mot',
                             precision = 0.01,
                             backlash = 0.07,
                             fmtstr = '%.2f',
                             unit = 'deg',
                            ),
)
