description = 'memograph readout'

includes = []

group = 'optional'

devices = dict(
    t_in_stressi = device('nicos_mlz.frm2.devices.memograph.MemographValue',
        hostname = 'memograph-uja04.care.frm2',
        group = 2,
        valuename = 'T_in StressSp',
        description = 'inlet temperature memograph',
        fmtstr = '%.2F',
        warnlimits = (-1, 17.5), #-1 no lower value
        unit = 'degC',
    ),
    t_out_stressi = device('nicos_mlz.frm2.devices.memograph.MemographValue',
        hostname = 'memograph-uja04.care.frm2',
        group = 2,
        valuename = 'T_out StressSp',
        description = 'outlet temperature memograph',
        pollinterval = 30,
        maxage = 60,
        fmtstr = '%.2F',
        unit = 'degC',
    ),
    p_in_stressi = device('nicos_mlz.frm2.devices.memograph.MemographValue',
        hostname = 'memograph-uja04.care.frm2',
        group = 2,
        valuename = 'P_in StressSp',
        description = 'inlet pressure memograph',
        pollinterval = 30,
        maxage = 60,
        fmtstr = '%.2F',
        unit = 'bar',
    ),
    p_out_stressi = device('nicos_mlz.frm2.devices.memograph.MemographValue',
        hostname = 'memograph-uja04.care.frm2',
        group = 2,
        valuename = 'P_out StressSp',
        description = 'outlet pressure memograph',
        pollinterval = 30,
        maxage = 60,
        fmtstr = '%.2F',
        unit = 'bar',
    ),
    flow_in_stressi = device('nicos_mlz.frm2.devices.memograph.MemographValue',
        hostname = 'memograph-uja04.care.frm2',
        group = 2,
        valuename = 'FLOW_in StressSp',
        description = 'inlet flow memograph',
        pollinterval = 30,
        maxage = 60,
        fmtstr = '%.2F',
        warnlimits = (0.2, 100), #100 no upper value
        unit = 'l/min',
    ),
    flow_out_stressi = device('nicos_mlz.frm2.devices.memograph.MemographValue',
        hostname = 'memograph-uja04.care.frm2',
        group = 2,
        valuename = 'FLOW_out StressS',
        description = 'outlet flow memograph',
        pollinterval = 30,
        maxage = 60,
        fmtstr = '%.2F',
        unit = 'l/min',
    ),
    leak_stressi   = device('nicos_mlz.frm2.devices.memograph.MemographValue',
        hostname = 'memograph-uja04.care.frm2',
        group = 2,
        valuename = 'Leak StressSp',
        description = 'leakage memograph',
        pollinterval = 30,
        maxage = 60,
        fmtstr = '%.2F',
        warnlimits = (-1, 1), #-1 no lower value
        unit = 'l/min',
    ),
    cooling_stressi = device('nicos_mlz.frm2.devices.memograph.MemographValue',
        hostname = 'memograph-uja04.care.frm2',
        group = 2,
        valuename = 'Cooling StressSp',
        description = 'cooling power memograph',
        pollinterval = 30,
        maxage = 60,
        fmtstr = '%.2F',
        unit = 'kW',
    ),
)
