description = 'FRM-II CCR box with LakeShore LS336 controller'

group = 'optional'

includes = ['alias_T']

nethost = 'ccr11'       # old style

devices = {
    'T_%s' % setupname : device('frm2.ccr.CCRControl',
                                        description = 'The main temperature control device of the ccr',
                                        stick = 'T_%s_stick' % setupname,
                                        tube = 'T_%s_tube' % setupname,
                                        unit = 'K',
                                        fmtstr = '%.3f',
                                        pollinterval = 5,
                                        maxage = 6,
                                       ),

    'T_%s_stick' % setupname : device('devices.taco.TemperatureController',
                                        description = 'The control device of the sample(stick)',
                                        tacodevice = '//%s/ccr/ls336/control2' % nethost,
                                        abslimits = (0, 600),
                                        unit = 'K',
                                        fmtstr = '%.3f',
                                        pollinterval = 5,
                                        maxage = 6,
                                       ),

    'T_%s_tube' % setupname : device('devices.taco.TemperatureController',
                                       description = 'The control device of the tube',
                                       tacodevice = '//%s/ccr/ls336/control1' % nethost,
                                       abslimits = (0, 300),
                                       warnlimits = (0, 300),
                                       unit = 'K',
                                       fmtstr = '%.3f',
                                       pollinterval = 5,
                                       maxage = 6,
                                      ),

    'T_%s_A' % setupname : device('devices.taco.TemperatureSensor',
                                   description = '(optional) Sample Temperature',
                                   tacodevice = '//%s/ccr/ls336/sensora' % nethost,
                                   unit = 'K',
                                   fmtstr = '%.3f',
                                   pollinterval = 5,
                                   maxage = 6,
                                  ),

    'T_%s_B' % setupname : device('devices.taco.TemperatureSensor',
                                   description = '(regulation) Temperature at the stick',
                                   tacodevice = '//%s/ccr/ls336/sensorb' % nethost,
                                   unit = 'K',
                                   fmtstr = '%.3f',
                                   pollinterval = 5,
                                   maxage = 6,
                                  ),

    'T_%s_C' % setupname : device('devices.taco.TemperatureSensor',
                                   description = 'Temperature of the coldhead',
                                   tacodevice = '//%s/ccr/ls336/sensorc' % nethost,
                                   warnlimits = (0, 300),
                                   unit = 'K',
                                   fmtstr = '%.3f',
                                   pollinterval = 5,
                                   maxage = 6,
                                  ),

    'T_%s_D' % setupname : device('devices.taco.TemperatureSensor',
                                   description = '(regulation) Temperature at thermal coupling to the stick',
                                   tacodevice = '//%s/ccr/ls336/sensord' % nethost,
                                   warnlimits = (0, 300),
                                   unit = 'K',
                                   fmtstr = '%.3f',
                                   pollinterval = 5,
                                   maxage = 6,
                                  ),

    '%s_compressor_switch' % setupname : device('devices.taco.DigitalOutput',
                                                 description = 'Switch for the compressor',
                                                 tacodevice = '//%s/ccr/plc/on' % nethost,
                                                ),

    '%s_gas_set' % setupname : device('devices.taco.DigitalOutput',
                                       description = 'Switch for the gas valve',
                                       lowlevel = True,
                                       tacodevice = '//%s/ccr/plc/gas' % nethost,
                                      ),

    '%s_gas_read' % setupname : device('devices.taco.DigitalInput',
                                        description = 'Read back of the gas valve state',
                                        lowlevel = True,
                                        tacodevice = '//%s/ccr/plc/fbgas' % nethost,
                                       ),

    '%s_gas_switch' % setupname : device('devices.vendor.frm2.CCRSwitch',
                                          description = 'Gas valve switch',
                                          write = '%s_gas_set' % nethost,
                                          feedback = '%s_gas_read' % nethost,
                                         ),

    '%s_vacuum_set' % setupname : device('devices.taco.DigitalOutput',
                                          description = 'Switch for the vacuum valve',
                                          lowlevel = True,
                                          tacodevice = '//%s/ccr/plc/vacuum' % nethost,
                                         ),

    '%s_vacuum_read' % setupname : device('devices.taco.DigitalInput',
                                           description = 'Read back of the vacuum valve state',
                                           lowlevel = True,
                                           tacodevice = '//%s/ccr/plc/fbvacuum' % nethost,
                                         ),

    '%s_vacuum_switch' % setupname : device('devices.vendor.frm2.CCRSwitch',
                                             description = 'Vacuum valve switch',
                                             write = '%s_vacuum_set' % nethost,
                                             feedback = '%s_vacuum_read' % nethost,
                                            ),

    '%s_p1' % setupname : device('devices.taco.AnalogInput',
                                  description = 'Pressure in sample space',
                                  tacodevice = '//%s/ccr/plc/p1' % nethost,
                                  fmtstr = '%.4g',
                                  pollinterval = 15,
                                  maxage = 20,
                                  unit = 'mbar',
                                 ),

    '%s_p2' % setupname : device('devices.taco.AnalogInput',
                                  description = 'Pressure in the vacuum chamber',
                                  tacodevice = '//%s/ccr/plc/p2' % nethost,
                                  fmtstr = '%.4g',
                                  pollinterval = 15,
                                  maxage = 20,
                                  unit = 'mbar',
                                 ),
}

startupcode = """
T.alias = T_%s
Ts.alias = T_%s_B
AddEnvironment(T, Ts)
""" % (setupname, setupname, )
