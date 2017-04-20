# -*- coding: utf-8 -*-

description = 'Selector area setup'
group = 'lowlevel'
display_order = 20

includes = ['sample']
excludes = ['virtual_selector']

sel_presets = configdata('config_selector.SELECTOR_PRESETS')
res_presets = configdata('config_resolution.RESOLUTION_PRESETS')

tango_base = 'tango://phys.kws3.frm2:10000/kws3/'

devices = dict(
    selector        = device('devices.generic.MultiSwitcher',
                             description = 'select selector presets',
                             blockingmove = False,
                             moveables = ['sel_lambda'],
                             mapping = {k: [v['lam']]
                                        for (k, v) in sel_presets.items()},
                             fallback = 'unknown',
                             precision = [0.05],
                            ),

    sel_speed_valid = device('devices.tango.DigitalOutput',
                             tangodevice = tango_base + 'fzjdp_digital/sel_speed_valid',
                             lowlevel = True,
                            ),
    sel_speed_status = device('devices.tango.DigitalInput',
                             tangodevice = tango_base + 'fzjdp_digital/sel_speed_status',
                             lowlevel = True,
                            ),
    sel_speed_set   = device('devices.tango.AnalogOutput',
                             tangodevice = tango_base + 'fzjdp_analog/sel_speed_set',
                             abslimits = (60, 300),
                             lowlevel = True,
                            ),
    sel_speed_read  = device('devices.tango.AnalogInput',
                             tangodevice = tango_base + 'fzjdp_analog/sel_speed_read',
                             lowlevel = True,
                            ),

    sel_speed       = device('kws3.selector.SelectorSpeed',
                             description = 'selector speed',
                             valid = 'sel_speed_valid',
                             speedset = 'sel_speed_set',
                             speedread = 'sel_speed_read',
                             status = 'sel_speed_status',
                             abslimits = (60, 300),
                             precision = 0.2,
                             unit = 'Hz',
                            ),

    sel_lambda      = device('kws1.selector.SelectorLambda',
                             description = 'Selector wavelength control',
                             seldev = 'sel_speed',
                             unit = 'A',
                             fmtstr = '%.2f',
                             constant = 3133.4 / 60,  # SelectorLambda uses RPM
                             offset = -0.00195,
                            ),

    sel_rot         = device('devices.tango.Motor',
                             description = 'selector rotation table',
                             tangodevice = tango_base + 'fzjs7/sel_rot',
                             unit = 'deg',
                             precision = 0.01,
                            ),

    resolution      = device('devices.generic.MultiSwitcher',
                             description = 'select resolution presets',
                             blockingmove = False,
                             moveables = ['sel_ap2', 'det_x', 'det_y', 'det_z'],
                             mapping = {k: [v['ap'], v['det_x'], v['det_y'], v['det_z']]
                                        for (k, v) in res_presets.items()},
                             fallback = 'unknown',
                             precision = [None, 0.01, 0.01, 0.01],
                            ),

    sel_ap1         = device('devices.generic.TwoAxisSlit',
                             description = 'aperture before selector',
                             fmtstr = '%.3f %.3f',
                             horizontal = 'sel_ap1_width',
                             vertical = 'sel_ap1_height',
                            ),
    sel_ap1_width   = device('devices.tango.Motor',
                             description = 'aperture selector horizontal opening',
                             tangodevice = tango_base + 'fzjs7/sel_ap1_x_delta',
                             unit = 'mm',
                             precision = 0.01,
                             lowlevel = True,
                            ),
    sel_ap1_height  = device('devices.tango.Motor',
                             description = 'aperture selector vertical opening',
                             tangodevice = tango_base + 'fzjs7/sel_ap1_y_delta',
                             unit = 'mm',
                             precision = 0.01,
                             lowlevel = True,
                            ),
    sel_ap2         = device('devices.generic.Slit',
                             description = 'selector jj-xray aperture',
                             coordinates = 'opposite',
                             left = 'sel_ap2_x_left',
                             right = 'sel_ap2_x_right',
                             bottom = 'sel_ap2_y_lower',
                             top = 'sel_ap2_y_upper',
                            ),
    sel_ap2_x_left  = device('devices.tango.Motor',
                             description = 'selector jj-xray aperture left',
                             tangodevice = tango_base + 'fzjs7/sel_ap2_x_left',
                             unit = 'mm',
                             precision = 0.1,
                             lowlevel = True,
                            ),
    sel_ap2_x_right = device('devices.tango.Motor',
                             description = 'selector jj-xray aperture right',
                             tangodevice = tango_base + 'fzjs7/sel_ap2_x_right',
                             unit = 'mm',
                             precision = 0.1,
                             lowlevel = True,
                            ),
    sel_ap2_y_upper = device('devices.tango.Motor',
                             description = 'selector jj-xray aperture upper',
                             tangodevice = tango_base + 'fzjs7/sel_ap2_y_upper',
                             unit = 'mm',
                             precision = 0.1,
                             lowlevel = True,
                            ),
    sel_ap2_y_lower = device('devices.tango.Motor',
                             description = 'selector jj-xray aperture lower',
                             tangodevice = tango_base + 'fzjs7/sel_ap2_y_lower',
                             unit = 'mm',
                             precision = 0.1,
                             lowlevel = True,
                            ),
)

extended = dict(
    poller_cache_reader = ['det_x', 'det_y', 'det_z'],
)

alias_config = {
    'sam_ap': {'sel_ap2': 80},
}