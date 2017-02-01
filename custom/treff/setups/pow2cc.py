# -*- coding: utf-8 -*-

description = "Toellner power supply 2 current setup"
group = "optional"

tango_base = "tango://phys.treff.frm2:10000/treff/"

excludes = ["pow2vc","virtual_polarizer"]

devices = dict(
    pow2comp  = device("devices.tango.PowerSupply",
                      description = "Power supply 2 current control ch 1",
                      tangodevice = tango_base + "toellner/pow2comp",
                     ),
    pow2flip  = device("devices.tango.PowerSupply",
                      description = "Power supply 2 current control ch 2",
                      tangodevice = tango_base + "toellner/pow2flip",
                     ),
    aflipper  = device("treff.flipper.Flipper",
                       description = "Analyzer flip",
                       flip = "pow2flip",
                       corr = "pow2comp",
                       currents = (1., 0.),
                      ),
 )
