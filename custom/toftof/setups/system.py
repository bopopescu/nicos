#  -*- coding: utf-8 -*-
description = 'NICOS system setup'

group = 'lowlevel'

sysconfig = dict(
    cache = 'tofhw.toftof.frm2',
    instrument = 'TOFTOF',
    experiment = 'Exp',
    datasinks = ['conssink', 'filesink', 'daemonsink'],
    notifiers = ['emailer', 'smser'],
)

modules = ['commands.standard']

includes = ['notifiers', ]

devices = dict(
    TOFTOF   = device('frm2.instrument.Instrument',
                      description = 'The famous TOFTOF instrument',
                      responsible = 'W. Lohstroh <wiebke.lohstroh@frm2.tum.de>',
                      instrument = 'TOFTOF',
                      doi = 'http://dx.doi.org/10.17815/jlsrf-1-40',
                      website = 'http://www.mlz-garching.de/toftof',
                      operators = [u'Technische Universität München (TUM)', ],
                     ),

    Sample   = device('devices.sample.Sample',
                      description = 'The current used sample',
                     ),

    Exp      = device('frm2.experiment.Experiment',
                      description = 'The current running experiment',
                      dataroot = '/data',
                      sample = 'Sample',
                      serviceexp = '0',
                      propprefix = '',
                      sendmail = True,
                      mailsender = 'nicos.toftof@frm2.tum.de',
                      propdb = '/opt/nicos/propdb',
                      managerights = dict(enableDirMode=0o775,
                                          enableFileMode=0o664,
                                          disableDirMode=0o550,
                                          disableFileMode=0o440,
                                          owner='nicd', group='nicd',
                                         ),
                      elog = True,
                      scancounter = 'scancounter',
                      # filecounter = '/data/counter',
                      imagecounter = 'counter',
                     ),

    filesink = device('devices.datasinks.AsciiDatafileSink',
                      lowlevel = True,
                     ),

    conssink = device('devices.datasinks.ConsoleSink',
                      lowlevel = True,
                     ),

    daemonsink = device('devices.datasinks.DaemonSink',
                        lowlevel = True,
                       ),

    Space    = device('devices.generic.FreeSpace',
                      description = 'The amount of free space for storing data',
                      path = '/data',
                      minfree = 5,
                     ),
)
