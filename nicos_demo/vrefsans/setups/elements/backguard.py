description = 'backguard: after sample'

group = 'optional'

devices = dict(
    backguard = device('nicos_mlz.refsans.devices.skew_motor.SkewMotor',
        description = description + ' adjust in Expertmode',
        motor_1 = 'backguard_1',
        motor_2 = 'backguard_2',
        abslimits = (-60, 60),
        unit = 'mm',
    ),
    backguard_1 = device('nicos.devices.generic.Axis',
        description = 'Backguard axis KWS. Use this to adjust KWS-side',
        motor = device('nicos.devices.generic.VirtualMotor',
            abslimits = (-0.5, 61.0),
            speed = 1,
            unit = 'mm',
        ),
        precision = 0.01,
        abslimits = (-60, 60),
        lowlevel = True,
    ),
    backguard_2 = device('nicos.devices.generic.Axis',
        description = 'Backguard axis TOFTOF. Use this to adjus TOFTOF-side',
        motor = device('nicos.devices.generic.VirtualMotor',
            abslimits = (-0.5, 61.0),
            speed = 1,
            unit = 'mm',
        ),
        precision = 0.01,
        abslimits = (-60, 60),
        lowlevel = True,
    ),
)