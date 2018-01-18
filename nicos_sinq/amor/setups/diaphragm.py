description = 'Diaphragms devices in the SINQ AMOR.'

pvprefix = 'SQ:AMOR:motc:'

devices = dict(
    d5v=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 5 vertical motor',
               motorpv=pvprefix + 'd5v',
               errormsgpv=pvprefix + 'd5v-MsgTxt',
               ),
    d5h=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 5 horizontal motor',
               motorpv=pvprefix + 'd5h',
               errormsgpv=pvprefix + 'd5h-MsgTxt',
               ),
    d1l=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 1 left motor',
               motorpv=pvprefix + 'd1l',
               errormsgpv=pvprefix + 'd1l-MsgTxt',
               ),
    d1r=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 1 right motor',
               motorpv=pvprefix + 'd1r',
               errormsgpv=pvprefix + 'd1r-MsgTxt',
               ),
    d3t=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 3 opening motor',
               motorpv=pvprefix + 'd3t',
               errormsgpv=pvprefix + 'd3t-MsgTxt',
               ),
    d3b=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 3 z position (lower edge) motor',
               motorpv=pvprefix + 'd3b',
               errormsgpv=pvprefix + 'd3b-MsgTxt',
               ),
    d4t=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 4 opening motor',
               motorpv=pvprefix + 'd4t',
               errormsgpv=pvprefix + 'd4t-MsgTxt',
               ),
    d4b=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 4 z position (lower edge) motor',
               motorpv=pvprefix + 'd4b',
               errormsgpv=pvprefix + 'd4b-MsgTxt',
               ),
    d1t=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 1 opening motor',
               motorpv=pvprefix + 'd1t',
               errormsgpv=pvprefix + 'd1t-MsgTxt',
               ),
    d1b=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 1 z position (lower edge) motor',
               motorpv=pvprefix + 'd1b',
               errormsgpv=pvprefix + 'd1b-MsgTxt',
               ),
    d2t=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 2 opening motor',
               motorpv=pvprefix + 'd2t',
               errormsgpv=pvprefix + 'd2t-MsgTxt',
               ),
    d2b=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms 2 z position (lower edge) motor',
               motorpv=pvprefix + 'd2b',
               errormsgpv=pvprefix + 'd2b-MsgTxt',
               ),
    dbs=device('nicos_ess.devices.epics.motor.EpicsMotor',
               epicstimeout=3.0,
               description='Diaphragms s (lower edge) motor',
               motorpv='SQ:AMOR:motb:dbs',
               errormsgpv='SQ:AMOR:motb:dbs-MsgTxt',
               ),
)
