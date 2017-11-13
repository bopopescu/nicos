description = "DoubleSlit [slit k1] between nok6 and nok7"

group = 'optional'

devices = dict(
    zb3r_m  = device('nicos.devices.generic.Axis',
        description = 'Axis of ZB3, reactor side',
        motor = device('nicos.devices.generic.virtual.VirtualMotor',
            abslimits = (-677.125, 99.125),
            userlimits = (-221.0, 95.0),
            speed = 5.,
            unit = 'mm',
        ),
        precision = 0.5,
        unit = 'mm',
    ),
    zb3r = device('nicos_mlz.refsans.devices.slits.SingleSlit',
        description = 'ZB3 slit, reactor side',
        motor = 'zb3r_m',
        nok_start = 8837.5,
        nok_length = 13.0,
        nok_end = 8850.5,
        nok_gap = 1.0,
        masks = {
            'slit': -0,
            'point': -0,
            'gisans': -110,
        },
        unit = 'mm',
    ),
    zb3s_m  = device('nicos.devices.generic.Axis',
        description = 'Axis of ZB3, sample side',
        motor = device('nicos.devices.generic.virtual.VirtualMotor',
            abslimits = (-150.8125, 113.5625),
            userlimits = (-106.0, 113.562),
            speed = 5.,
            unit = 'mm',
        ),
        precision = 0.5,
        unit = 'mm',
    ),
    zb3s = device('nicos_mlz.refsans.devices.slits.SingleSlit',
        description = 'ZB3 slit, sample side',
        motor = 'zb3s_m',
        nok_start = 8837.5,
        nok_length = 13.0,
        nok_end = 8850.5,
        nok_gap = 1.0,
        masks = {
            'slit': -0,
            'point': -0,
            'gisans': -110,
        },
        unit = 'mm',
    ),
)