
description = 'Sample table devices'

group = 'optional'

nethost = 'refsanssrv.refsans.frm2'
tacodev = '//%s/test' % nethost


devices = dict(
    theta = device('devices.generic.Axis',
                   description = 'Theta axis',
                   motor = 'theta_m',
                   coder = 'theta_m',
                   precision = 0.01,
                  ),
    theta_m = device('devices.taco.Motor',
                     description = 'Theta axis motor',
                     tacodevice = '%s/phytron/kanal_01' % tacodev,
                     abslimits = (-2, 10),
                     lowlevel = True,
                    ),
    phi = device('devices.generic.Axis',
                 description = 'Phi axis',
                 motor = 'phi_m',
                 coder = 'phi_m',
                 precision = 0.01,
                ),
    phi_m = device('devices.taco.Motor',
                   description = 'Phi axis motor',
                   tacodevice = '%s/phytron/kanal_02' % tacodev,
                   abslimits = (-9.75, 9.5),
                   lowlevel = True,
                  ),
    chi = device('devices.generic.Axis',
                 description = 'Chi axis',
                 motor = 'chi_m',
                 coder = 'chi_m',
                 precision = 0.01,
                ),
    chi_m = device('devices.taco.Motor',
                   description = 'Chi axis motor',
                   tacodevice = '%s/phytron/kanal_03' % tacodev,
                   abslimits = (-2.5, 2.5),
                   lowlevel = True,
                  ),
    y = device('devices.generic.Axis',
               description = 'Y axis',
               motor = 'y_m',
               coder = 'y_m',
               precision = 0.01,
              ),
    y_m = device('devices.taco.Motor',
                 description = 'Y axis motor',
                 tacodevice = '%s/phytron/kanal_04' % tacodev,
                 abslimits = (-78.0, 75.0),
                 lowlevel = True,
                ),
    z = device('devices.generic.Axis',
               description = 'Z axis',
               motor = 'z_m',
               coder = 'z_m',
               precision = 0.01,
              ),
    z_m = device('devices.taco.Motor',
                 description = 'Z axis motor',
                 tacodevice = '%s/phytron/kanal_05' % tacodev,
                 abslimits = (-300.0, 188.0),
                 lowlevel = True,
                ),
    probenwechsler = device('devices.generic.Axis',
                            description = 'Samplechanger axis',
                            motor = 'probenwechsler_m',
                            coder = 'probenwechsler_m',
                            precision = 0.01,
                           ),
    probenwechsler_m = device('devices.taco.Motor',
                              description = 'Samplechanger axis motor',
                              tacodevice = '%s/phytron/kanal_06' % tacodev,
                              abslimits = (-.5, 400.5),
                              lowlevel = True,
                             ),
    bg = device('devices.taco.Motor',
                description = 'Backgard axis motor',
                tacodevice = '%s/phytron/kanal_07' % tacodev,
                abslimits = (-0.5, 31.0),
               ),
    # = device('devices.taco.Motor',
    #          description = ' axis motor',
    #          tacodevice = '%s/phytron/kanal_' % tacodev,
    #          abslimits = (),
    #         ),
    monitor = device('devices.taco.Motor',
                     description = 'Monitor axis motor',
                     tacodevice = '%s/phytron/kanal_09' % tacodev,
                     abslimits = (10, 300),
                    ),
    top_theta = device('devices.taco.Motor',
                       description = 'Top Theta axis motor',
                       tacodevice = '%s/phytron/kanal_10' % tacodev,
                       abslimits = (-9.5, 10.5),
                      ),
    top_z = device('devices.taco.Motor',
                   description = 'Top Z axis motor',
                   tacodevice = '%s/phytron/kanal_11' % tacodev,
                   abslimits = (-0.05, 15),
                  ),
    top_phi = device('devices.taco.Motor',
                     description = 'Top Phi axis motor',
                     tacodevice = '%s/phytron/kanal_12' % tacodev,
                     abslimits = (-10.5, 10.5),
                    ),
)