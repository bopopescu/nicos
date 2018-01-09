description = 'Gas flow for the (Cascade) PSD detector'
group = 'lowlevel'

includes = []

tango_base = 'tango://resedahw2.reseda.frm2:10000/reseda/'

devices = dict(
    ar = device('nicos.devices.tango.AnalogOutput',
        description = 'Ar gas flow through the detector',
        tangodevice = tango_base + 'gasmix/arflow',
        userlimits = (0, 250),
        unit = 'mln/min',
    ),
    ar_temp = device('nicos.devices.tango.Sensor',
        description = 'Ar gas temperature (through the detector)',
        tangodevice = tango_base + 'gasmix/artemp',
        unit = 'C',
    ),
    co2 = device('nicos.devices.tango.AnalogOutput',
        description = 'CO2 gas flow through the detector',
        tangodevice = tango_base + 'gasmix/co2flow',
        userlimits = (0, 50),
        unit = 'mln/min',
    ),
    co2_temp = device('nicos.devices.tango.Sensor',
        description = 'CO2 gas temperature (through the detector)',
        tangodevice = tango_base + 'gasmix/co2temp',
        unit = 'C',
    ),
)
