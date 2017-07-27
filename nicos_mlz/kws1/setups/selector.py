#  -*- coding: utf-8 -*-

description = 'setup for the velocity selector'
group = 'lowlevel'
display_order = 15

excludes = ['virtual_selector']

presets = configdata('config_selector.SELECTOR_PRESETS')

tango_base = 'tango://phys.kws1.frm2:10000/kws1/'

devices = dict(
    selector        = device('nicos_mlz.kws1.devices.selector.SelectorSwitcher',
                             description = 'select selector presets',
                             blockingmove = False,
                             moveables = ['selector_speed'],
                             det_pos = 'detector',
                             presets = presets,
                             mapping = dict((k, [v['speed']])
                                            for (k, v) in presets.items()),
                             fallback = 'unknown',
                             precision = [10.0],
                            ),

    selector_speed  = device('nicos_mlz.kws1.devices.selector.SelectorSpeed',
                             description = 'Selector speed control',
                             tangodevice = tango_base + 'selector/speed',
                             unit = 'rpm',
                             fmtstr = '%.0f',
                             warnlimits = (6500, 27300),
                             abslimits = (6500, 27300),
                             precision = 10,
                             window = 30,
                             timeout = 300.0,
                            ),

    selector_lambda = device('nicos_mlz.kws1.devices.selector.SelectorLambda',
                             description = 'Selector wavelength control',
                             seldev = 'selector_speed',
                             unit = 'A',
                             fmtstr = '%.2f',
                             constant = 2227.5,
                            ),

    selector_rtemp  = device('nicos.devices.tango.AnalogInput',
                             description = 'Temperature of the selector rotor',
                             tangodevice = tango_base + 'selector/rotortemp',
                             unit = 'degC',
                             fmtstr = '%.1f',
                             warnlimits = (10, 40),
                             lowlevel = True,
                            ),
    selector_winlt  = device('nicos.devices.tango.AnalogInput',
                             description = 'Cooling water temperature at inlet',
                             tangodevice = tango_base + 'selector/waterintemp',
                             unit = 'degC',
                             fmtstr = '%.1f',
                             warnlimits = (15, 22),
                             lowlevel = True,
                            ),
    selector_woutt  = device('nicos.devices.tango.AnalogInput',
                             description = 'Cooling water temperature at outlet',
                             tangodevice = tango_base + 'selector/waterouttemp',
                             unit = 'degC',
                             fmtstr = '%.1f',
                             warnlimits = (15, 26),
                             lowlevel = True,
                            ),
    selector_wflow  = device('nicos.devices.tango.AnalogInput',
                             description = 'Cooling water flow rate through selector',
                             tangodevice = tango_base + 'selector/flowrate',
                             unit = 'l/min',
                             fmtstr = '%.1f',
                             warnlimits = (1.0, 10),
                             lowlevel = True,
                            ),
    selector_vacuum = device('nicos.devices.tango.AnalogInput',
                             description = 'Vacuum in the selector',
                             tangodevice = tango_base + 'selector/vacuum',
                             unit = 'mbar',
                             fmtstr = '%.5f',
                             warnlimits = (0, 0.02),
                             lowlevel = True,
                            ),
    selector_vibrt  = device('nicos.devices.tango.AnalogInput',
                             description = 'Selector vibration',
                             tangodevice = tango_base + 'selector/vibration',
                             unit = 'mm/s',
                             fmtstr = '%.2f',
                             warnlimits = (0, 0.6),
                             lowlevel = True,
                            ),
)

extended = dict(
    poller_cache_reader = ['detector'],
)