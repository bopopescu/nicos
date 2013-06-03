description = 'chopper setup'

group = 'lowlevel'

includes = []

devices = dict(
    ch           = device('toftof.chopper.Controller',
                          tacodevice = '//toftofsrv/toftof/rs232/ifchoppercontrol',
                          speed_accuracy = 2,
                          phase_accuracy = 10,
                          ch5_90deg_offset = 0,
                          timeout = 600,
                          pollinterval = 10,
                          maxage = 12,
                         ),
    chWL         = device('toftof.chopper.Wavelength',
                          description = 'Neutron wavelength',
                          chopper = 'ch',
                          abslimits = (0.2, 16.0),
                          pollinterval = 10,
                          maxage = 12,
                          unit = 'rpm',
                         ),
    chSpeed      = device('toftof.chopper.Speed',
                          description = 'Setpoint of the chopper speed',
                          chopper = 'ch',
                          abslimits = (0, 22000.),
                          pollinterval = 10,
                          maxage = 12,
                          unit = 'rpm',
                         ),
    chRatio      = device('toftof.chopper.Ratio',
                          description = 'Frame overlap ratio',
                          chopper = 'ch',
                          pollinterval = 10,
                          maxage = 12,
                         ),
    chCRC        = device('toftof.chopper.CRC',
                          description = 'Chopper rotation sense (CRC=1, '
                                        'parallel=0)',
                          requires = {'level': 'admin'},
                          chopper = 'ch',
                          pollinterval = 10,
                          maxage = 12,
                         ),
    chST         = device('toftof.chopper.SlitType',
                          description = 'Chopper window; large window=0',
                          requires = {'level': 'admin'},
                          chopper = 'ch',
                          pollinterval = 10,
                          maxage = 12,
                         ),
    chDS         = device('toftof.chopper.SpeedReadout',
                          description = 'Speed of the disks 1 - 7',
                          chopper = 'ch',
                          fmtstr = '[%7.2f, %7.2f, %7.2f, %7.2f, %7.2f, %7.2f, %7.2f]',
                          pollinterval = 10,
                          maxage = 12,
                          unit = 'rpm',
                         ),

    chdelaybus   = device('devices.vendor.toni.ModBus',
                          tacodevice = 'toftof/rs232/ifchdelay',
                          lowlevel = True,
                         ),
    chdelay      = device('devices.vendor.toni.DelayBox',
                          description = 'Trigger time-offset',
                          requires = {'level': 'guest'},
                          bus = 'chdelaybus',
                          addr = 0xF1,
                          unit = 'usec',
                          fmtstr = '%d',
                         ),
)
