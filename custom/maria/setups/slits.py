# -*- coding: utf-8 -*-

description = "Slits setup"
group = "optional"

tango_base = "tango://phys.maria.frm2:10000/maria"
tango_pi = tango_base + "/piaperture"
tango_s7 = tango_base + "/FZJS7"
tango_analog = tango_base + "/FZJDP_Analog"

devices = dict(
    s1_left = device("devices.tango.Motor",
        description = "slit s1 left",
        tangodevice = tango_pi + "/s1_left",
        precision = 0.001,
        fmtstr = "%.3f",
    ),
    s1_right = device("devices.tango.Motor",
        description = "slit s1 right",
        tangodevice = tango_pi + "/s1_right",
        precision = 0.001,
        fmtstr = "%.3f",
    ),
    s1_bottom = device("devices.tango.Motor",
        description = "slit s1 bottom",
        tangodevice = tango_s7 + "/s1_bottom",
        precision = 0.01,
        fmtstr = "%.3f",
    ),
    s1_top = device("devices.tango.Motor",
        description = "slit s1 top",
        tangodevice = tango_s7 + "/s1_top",
        precision = 0.01,
        fmtstr = "%.3f",
    ),
    s2_left = device("devices.tango.Motor",
        description = "slit s2 left",
        tangodevice = tango_pi + "/s2_left",
        precision = 0.001,
    ),
    s2_right = device("devices.tango.Motor",
        description = "slit s2 right",
        tangodevice = tango_pi + "/s2_right",
        precision = 0.001,
        fmtstr = "%.3f",
    ),
    s2_bottom = device("nicos.devices.generic.Axis",
        description = "slit s2 bottom",
        motor = "s2_bottom_mot",
        obs = "s2_bottom_cod",
        precision = 0.01,
        fmtstr = "%.3f",
    ),
    s2_bottom_mot = device("devices.tango.Motor",
        description = "slit s2 bottom motor",
        tangodevice = tango_s7 + "/s2_bottom",
        precision = 0.01,
        fmtstr = "%.3f",
        lowlevel = True,
    ),
    s2_bottom_cod = device("devices.tango.Sensor",
        description = "slit s2 bottom poti",
        tangodevice = tango_analog + "/s2_bottom",
        fmtstr = "%.3f",
        unit = "mm",
        pollinterval = 5,
        maxage = 6,
        lowlevel = True,
    ),
    s2_top = device("nicos.devices.generic.Axis",
        description = "slit s2 top",
        motor = "s2_top_mot",
        obs = "s2_top_cod",
        precision = 0.01,
        fmtstr = "%.3f",
    ),
    s2_top_mot = device("devices.tango.Motor",
        description = "slit s2 top motor",
        tangodevice = tango_s7 + "/s2_top",
        precision = 0.01,
        fmtstr = "%.3f",
        lowlevel = True,
    ),
    s2_top_cod = device("devices.tango.Sensor",
        description = "slit s2 top poti",
        tangodevice = tango_analog + "/s2_top",
        fmtstr = "%.3f",
        unit = "mm",
        pollinterval = 5,
        maxage = 6,
        lowlevel = True,
    ),
    ds_left = device("devices.tango.Motor",
        description = "detector slit left",
        tangodevice = tango_s7 + "/ds_left",
        precision = 0.001,
        fmtstr = "%.3f",
    )
)
