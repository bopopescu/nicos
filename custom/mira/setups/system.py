name = 'system setup only'

sysconfig = dict(
    cache = 'mira1',
    instrument = 'mira',
    experiment = 'Exp',
    notifiers = ['email', 'smser'],
    datasinks = ['conssink', 'filesink', 'dmnsink', 'gracesink'],
)

devices = dict(
    email    = device('nicos.notify.Mailer',
                      sender = 'nicos@mira1',
                      copies = ['rgeorgii@frm2.tum.de'],
                      subject = 'MIRA'),

    smser    = device('nicos.notify.SMSer',
                      server='triton.admin.frm2'),

    Exp      = device('nicos.mira.experiment.MiraExperiment',
                      sample = 'Sample',
                      datapath = ['/data/testdata'],
                      _propdb = 'useroffice@tacodb.taco.frm2:useroffice'),

    filesink = device('nicos.data.AsciiDatafileSink'),

    conssink = device('nicos.data.ConsoleSink'),

    dmnsink  = device('nicos.data.DaemonSink'),

    gracesink= device('nicos.data.GraceSink'),
)
