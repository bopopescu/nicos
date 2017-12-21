description = 'setup for VM4 magnet'

group = 'plugplay'
includes = ['alias_sth', 'alias_T']

tango_base = 'tango://%s:10000/box/' % setupname

devices = dict(
    vm4_pvti = device('nicos.devices.tango.Sensor',
        description = 'VTI pressure',
        tangodevice = tango_base + 'needlevalve/pressure',
        fmtstr = '%.3g',
    ),
    vm4_lhe = device('nicos.devices.tango.Sensor',
        description = 'Liquid helium level',
        tangodevice = tango_base + 'beckhoff/lhe',
        fmtstr = '%.1f',
        warnlimits = (20, 100),
    ),
    vm4_ln2 = device('nicos.devices.tango.Sensor',
        description = 'Liquid nitrogen level',
        tangodevice = tango_base + 'levelmeter/ln2',
        fmtstr = '%.1f',
        warnlimits = (20, 100),
    ),
    T_vm4_vti = device('nicos.devices.tango.TemperatureController',
        description = 'VTI temperature',
        tangodevice = tango_base + 'ls340/ctrl',
        unit = 'K',
    ),
    T_vm4_sample = device('nicos.devices.tango.Sensor',
        description = 'Sample thermometer temperature',
        tangodevice = tango_base + 'ls340/sensb',
        unit = 'K',
    ),
    T_vm4_vti_range = device('nicos.devices.tango.NamedDigitalOutput',
        description = 'Heater range for VTI',
        tangodevice = tango_base + 'ls340/range',
        warnlimits = ('high', 'medium'),
        mapping = {'off': 0,
                   '5mW': 1,
                   '50mW': 2,
                   '0.5W': 3,
                   '5W': 4,
                   '50W': 5},
        unit = '',
    ),
    vm4_nv_reg = device('nicos.devices.tango.Actuator',
        description = 'Needle valve regulation setpoint',
        tangodevice = tango_base + 'needlevalve/pressure_ctrl',
        unit = 'mbar',
    ),
    vm4_nv_manual = device('nicos.devices.tango.Actuator',
        description = 'Needle valve opening',
        tangodevice = tango_base + 'needlevalve/position_ctrl',
    ),
    # I_vm4 = device('nicos.devices.tango.Actuator',
    #     description = 'Current in the magnet',
    #     tangodevice = tango_base + 'ips/field',
    #     precision = 60,
    # ),
    # I_vm4_supply = device('nicos.devices.tango.Sensor',
    #     description = 'Current output of the power supply',
    #     tangodevice = tango_base + 'ips/actual',
    # ),
    co_sth_vm4 = device('nicos.devices.tango.Sensor',
        lowlevel = True,
        tangodevice = tango_base + 'sth/encoder',
        unit = 'deg',
    ),
    mo_sth_vm4 = device('nicos.devices.tango.Motor',
        lowlevel = True,
        tangodevice = tango_base + 'sth/motor',
        unit = 'deg',
        precision = 0.001,
    ),
    sth_vm4 = device('nicos.devices.generic.Axis',
        description = 'sample theta angle',
        motor = 'mo_sth_vm4',
        coder = 'co_sth_vm4',
        obs = [],
        fmtstr = '%.3f',
        precision = 0.01,
    ),
)

alias_config = {
    'sth': {'sth_vm4': 0},
    'T': {'T_vm4_vti': 200},
    'Ts': {'T_vm4_sample': 100},
}
