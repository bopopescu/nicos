description = 'setup for the NICOS watchdog'
group = 'special'

# The entries in this list are dictionaries. Possible keys:
#
# 'setup' -- setup that must be loaded (default '' to mean all setups)
# 'condition' -- condition for warning (a Python expression where cache keys
#    can be used: t_value stands for t/value etc.
# 'gracetime' -- time in sec allowed for the condition to be true without
#    emitting a warning (default 5 sec)
# 'message' -- warning message to display
# 'priority' -- 1 or 2, where 2 is more severe (default 1)
# 'action' -- code to execute if condition is true (default no code is executed)

watchlist = [
#    dict(condition = 'cooltemp_value > 30',
#         message = 'Cooling water temperature exceeds 30C, check FAK40 or MIRA Leckmon!',
#         type = 'critical',
#    ),
    dict(condition = 'TBeFilter_value > 80 and TBeFilter_value < 1000',
         message = 'Be filter temperature > 80 K, check cooling!',
         type = 'critical',
         setup = 'befilter',
    ),
    dict(condition = 'TBeFilter_value > 1000',
         message = 'Be filter thermometer disconnected',
         gracetime = 600,
         setup = 'befilter',
    ),
    dict(condition = 'T_heaterpower < 0.000001 and T_setpoint > 0.5',
         message = 'PROBLEM with heater - not heating - check PANDA',
         gracetime = 300,
         type = 'onlypetr',
         setup = 'cryo5',
    ),
    dict(condition = 'T_heaterpower > 0.002',
         message = 'PROBLEM with heater - heating too much - check PANDA',
         gracetime = 300,
         type = 'onlypetr',
         setup = 'cryo5',
    ),
    dict(condition = 'T_value > 320',
         message = 'PROBLEM temperature readout - RESTART lakeshore',
         gracetime = 10,
         type = 'onlypetr',
         setup = 'cryo5',
    ),
    dict(condition = '(t_ccr11_a_value < 0.1)',
         message = 'PROBLEM with TACO - automatically restarting',
         gracetime = 100,
         type = 'onlypetr',
         setup = 'ccr11',
         action = 'T_ccr11_A.reset();T_ccr11_B.reset();T_ccr11_C.reset();T_ccr11_D.reset();T_ccr11_tube.reset();T_ccr11.reset()',
    ),
    dict(condition = '(t_ccr11_c_value < 0.1)',
         message = 'PROBLEM with TACO - automatically restarting',
         gracetime = 100,
         type = 'onlypetr',
         setup = 'ccr11',
         action = 'T_ccr11_A.reset();T_ccr11_B.reset();T_ccr11_C.reset();T_ccr11_D.reset();T_ccr11_tube.reset();T_ccr11.reset()',
    ),
    #~ dict(condition = '(t_ccr11_d_value < 0.1)',
         #~ message = 'PROBLEM with TACO - automatically restarting',
         #~ gracetime = 100,
         #~ type = 'onlypetr',
         #~ setup = 'ccr11',
         #~ action = 'T_ccr11_A.reset();T_ccr11_B.reset();T_ccr11_C.reset();T_ccr11_D.reset();T_ccr11_tube.reset();T_ccr11.reset()',
    #~ ),
    #~ dict(condition = '(t_ccr11_tube_value < 0.1)',
         #~ message = 'PROBLEM with TACO - automatically restarting',
         #~ gracetime = 100,
         #~ type = 'onlypetr',
         #~ setup = 'ccr11',
         #~ action = 'T_ccr11_A.reset();T_ccr11_B.reset();T_ccr11_C.reset();T_ccr11_D.reset();T_ccr11_tube.reset();T_ccr11.reset()',
    #~ ),
    #~ dict(condition = '(t_ccr11_value < 0.1)',
         #~ message = 'PROBLEM with TACO - automatically restarting',
         #~ gracetime = 100,
         #~ type = 'onlypetr',
         #~ setup = 'ccr11',
         #~ action = 'T_ccr11_A.reset();T_ccr11_B.reset();T_ccr11_C.reset();T_ccr11_D.reset();T_ccr11_tube.reset();T_ccr11.reset()',
    #~ ),
]


# The Watchdog device has two lists of notifiers, one for priority 1 and
# one for priority 2.

devices = dict(
    email    = device('devices.notifiers.Mailer',
                      sender = 'panda@frm2.tum.de',
                      receivers = ['pcermak@frm2.tum.de', 'fstoica@frm2.tum.de', 'astrid.schneidewind@frm2.tum.de'],
                      subject = '[PANDA warning]',
                      loglevel='debug',
                     ),

    email2  = device('devices.notifiers.Mailer',
                      sender = 'panda@frm2.tum.de',
                      receivers = ['pcermak@frm2.tum.de'],
                      subject = '[PANDA]',
                      loglevel='debug',
                     ),

    email3  = device('devices.notifiers.Mailer',
                      sender = 'panda@frm2.tum.de',
                      receivers = ['astrid.schneidewind@frm2.tum.de'],
                      subject = '[PANDA]',
                      loglevel='debug',
                     ),

    smser    = device('devices.notifiers.SMSer',
                      server = 'triton.admin.frm2',
                      receivers = ['017697526049', '015252646651'],
                      loglevel='debug',
                     ),

    Watchdog = device('services.watchdog.Watchdog',
                      cache = 'pandasrv:14869',
                      notifiers = {'default': ['email'],
                                   'critical': ['email', 'smser'],
                                   'onlypetr': ['email2'],
                                   'onlyastrid': ['email3']},
                      watch = watchlist,
                      mailreceiverkey = 'email/receivers',
                      loglevel='debug',
                     ),
)
