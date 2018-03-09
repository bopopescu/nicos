description = 'Diaphragms devices in the SINQ AMOR.'

pvprefix = 'SQ:AMOR:motc:'

devices = dict(
    d5v=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 5 vertical motor',
               motorpv=pvprefix + 'd5v',
               errormsgpv=pvprefix + 'd5v-MsgTxt',
               lowlevel=True
               ),
    d5h=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 5 horizontal motor',
               motorpv=pvprefix + 'd5h',
               errormsgpv=pvprefix + 'd5h-MsgTxt',
               lowlevel=True
               ),
    d1l=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 1 left motor',
               motorpv=pvprefix + 'd1l',
               errormsgpv=pvprefix + 'd1l-MsgTxt',
               lowlevel=True
               ),
    d1r=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 1 right motor',
               motorpv=pvprefix + 'd1r',
               errormsgpv=pvprefix + 'd1r-MsgTxt',
               lowlevel=True
               ),
    d3t=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 3 opening motor',
               motorpv=pvprefix + 'd3t',
               errormsgpv=pvprefix + 'd3t-MsgTxt',
               lowlevel=True
               ),
    d3b=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 3 z position (lower edge) motor',
               motorpv=pvprefix + 'd3b',
               errormsgpv=pvprefix + 'd3b-MsgTxt',
               lowlevel=True
               ),
    d4t=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 4 opening motor',
               motorpv=pvprefix + 'd4t',
               errormsgpv=pvprefix + 'd4t-MsgTxt',
               lowlevel=True
               ),
    d4b=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 4 z position (lower edge) motor',
               motorpv=pvprefix + 'd4b',
               errormsgpv=pvprefix + 'd4b-MsgTxt',
               lowlevel=True
               ),
    d1t=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 1 opening motor',
               motorpv=pvprefix + 'd1t',
               errormsgpv=pvprefix + 'd1t-MsgTxt',
               lowlevel=True
               ),
    d1b=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 1 z position (lower edge) motor',
               motorpv=pvprefix + 'd1b',
               errormsgpv=pvprefix + 'd1b-MsgTxt',
               lowlevel=True
               ),
    d2t=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 2 opening motor',
               motorpv=pvprefix + 'd2t',
               errormsgpv=pvprefix + 'd2t-MsgTxt',
               lowlevel=True
               ),
    d2b=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 2 z position (lower edge) motor',
               motorpv=pvprefix + 'd2b',
               errormsgpv=pvprefix + 'd2b-MsgTxt',
               lowlevel=True
               ),
    slit1=device('nicos.devices.generic.slit.Slit',
                 description='Slit 1 with left, right, bottom and top motors',
                 opmode='4blades',
                 left='d1l',
                 right='d1r',
                 top='d1t',
                 bottom='d1b',
                 ),
    slit2=device('nicos.devices.generic.slit.Slit',
                 description='Slit 2 with left, right, bottom and top motors',
                 opmode='4blades',
                 left='d1l',
                 right='d1r',
                 top='d2t',
                 bottom='d2b',
                 ),
    slit3=device('nicos.devices.generic.slit.Slit',
                 description='Slit 3 with left, right, bottom and top motors',
                 opmode='4blades',
                 left='d1l',
                 right='d1r',
                 top='d3t',
                 bottom='d3b',
                 ),
    slit4=device('nicos.devices.generic.slit.Slit',
                 description='Slit 4 with left, right, bottom and top motors',
                 opmode='4blades',
                 left='d1l',
                 right='d1r',
                 top='d4t',
                 bottom='d4b',
                 ),
    slit5=device('nicos.devices.generic.slit.TwoAxisSlit',
                 description='Slit 5 with horizontal and vertical motors',
                 horizontal='d5h',
                 vertical='d5v'
                 ),
)
