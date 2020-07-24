description = 'TsDau detector'

connection = '192.168.1.6:10000'

devices = dict(
    tsd_timer=device('nicos_ess.v20.devices.tsdau.TsDauTimeChannel',
                     description='Time channel of TsDau detector.',
                     host=connection,
                     remoteobj='device',
                     ismain=True,
                     ),
    tsd_filename=device('nicos_ess.v20.devices.tsdau.TsDauFilenameChannel',
                        description='File name of Tsdau detector',
                        directory='',
                        host=connection,
                        remoteobj='device',
                        ismain=False
                        ),
    tsd_counter=device('nicos_ess.v20.devices.tsdau.TsDauCounterChannel',
                       description='Counter channel of TsDau detector',
                       host=connection,
                       remoteobj='device',
                       ismain=False,
                       type='counter'
                       ),
    tsdau=device('nicos_ess.v20.devices.tsdau.TsDauDetector',
                 description='TS Dau detector',
                 timers=['tsd_timer'],
                 counters=['tsd_counter'],
                 others=['tsd_filename'])
)
