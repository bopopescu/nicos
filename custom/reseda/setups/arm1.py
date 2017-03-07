#  -*- coding: utf-8 -*-

description = 'Arm 1 (NRSE)'
group = 'optional'

taco_base = '//resedasrv.reseda.frm2/reseda'
tango_base = 'tango://resedahw2.reseda.frm2:10000/reseda'

devices = dict(
    arm1_rot_mot = device('devices.taco.Motor',
        description = 'Rotation arm 1 (motor)',
        tacodevice = '%s/husco1/motor1' % taco_base,
        fmtstr = '%.3f',
        lowlevel=True,
    ),
    arm1_rot_enc = device('devices.taco.Coder',
        description = 'Rotation arm 1 (encoder)',
        tacodevice = '%s/enc/det1_1' % taco_base, # not enc/arm1 due to broken hw
        fmtstr = '%.3f',
        lowlevel=True,
    ),
    arm1_rot_air = device('devices.tango.DigitalOutput',
        description = 'Rotation arm 1 (air)',
        tangodevice = '%s/iobox/plc_air_a1' % tango_base,
        fmtstr = '%.3f',
        lowlevel=True,
    ),
    arm1_rot = device('mira.axis.HoveringAxis',
        description = 'Rotation arm 1',
        motor = 'arm1_rot_mot',
        coder = 'arm1_rot_enc',
        switch = 'arm1_rot_air',
        startdelay=2.0,
        stopdelay=2.0,
        fmtstr = '%.3f',
        precision = 0.1,
    ),
    T_arm1_coil1 = device('devices.tango.AnalogInput',
        description = 'Arm 1 coil 1 temperature',
        tangodevice = '%s/iobox/plc_t_arm1coil1' % tango_base,
        fmtstr = '%.3f',
    ),
    T_arm1_coil2 = device('devices.tango.AnalogInput',
        description = 'Arm 1 coil 2 temperature',
        tangodevice = '%s/iobox/plc_t_arm1coil2' % tango_base,
        fmtstr = '%.3f',
    ),
    T_arm1_coil3 = device('devices.tango.AnalogInput',
        description = 'Arm 1 coil 3 temperature',
        tangodevice = '%s/iobox/plc_t_arm1coil3' % tango_base,
        fmtstr = '%.3f',
    ),
    T_arm1_coil4 = device('devices.tango.AnalogInput',
        description = 'Arm 1 coil 4 temperature',
        tangodevice = '%s/iobox/plc_t_arm1coil4' % tango_base,
        fmtstr = '%.3f',
    ),
)