description = 'devices for fast detector using comtec p7888 for REFSANS'

# to be included by refsans?
group = 'optional'

nethost = 'refsanssrv.refsans.frm2'
tacodev = '//%s/test/fast' % nethost

sysconfig = dict(
    datasinks = ['conssink', 'filesink', 'daemonsink', 'RawFileSaver'],
)

devices = dict(
    fastctr_a = device('refsans.detector.ComtecCounter',
                       description = "Channel A of Comtep P7888 Fast Counter",
                       tacodevice = '%s/rate_a' % tacodev,
                       lowlevel = True,
                      ),
    fastctr_b = device('refsans.detector.ComtecCounter',
                       description = "Channel B of Comtep P7888 Fast Counter",
                       tacodevice = '%s/rate_b' % tacodev,
                       lowlevel = True,
                      ),
    fastctr_c = device('refsans.detector.ComtecCounter',
                       description = "Channel C of Comtep P7888 Fast Counter",
                       tacodevice = '%s/rate_c' % tacodev,
                       lowlevel = True,
                      ),
    fastctr_d = device('refsans.detector.ComtecCounter',
                       description = "Channel D of Comtep P7888 Fast Counter",
                       tacodevice = '%s/rate_d' % tacodev,
                       lowlevel = True,
                      ),
    fastctr_e = device('refsans.detector.ComtecCounter',
                       description = "Channel E of Comtep P7888 Fast Counter",
                       tacodevice = '%s/rate_e' % tacodev,
                       lowlevel = True,
                      ),
    fastctr_f = device('refsans.detector.ComtecCounter',
                       description = "Channel F of Comtep P7888 Fast Counter",
                       tacodevice = '%s/rate_f' % tacodev,
                       lowlevel = True,
                      ),
    fastctr_g = device('refsans.detector.ComtecCounter',
                       description = "Channel G of Comtep P7888 Fast Counter",
                       tacodevice = '%s/rate_g' % tacodev,
                       lowlevel = True,
                      ),
    fastctr_h = device('refsans.detector.ComtecCounter',
                       description = "Channel H of Comtep P7888 Fast Counter",
                       tacodevice = '%s/rate_h' % tacodev,
                       lowlevel = True,
                      ),
    RawFileSaver  = device('refsans.detector.ComtecFileFormat',
                           description = 'Saves image data in RAW format',
                           filenametemplate = ['%(proposal)s_%(counter)s.cfg',
                                      '%(proposal)s_%(session.experiment.lastscan)s'
                                      '_%(counter)s_%(scanpoint)s.cfg'],
                           lowlevel = True,
                          ),
    comtec_timer    = device('refsans.detector.ComtecTimer',
                       description = 'Comtec P7888 Fast System: Timer channel',
                       tacodevice = '%s/detector' % tacodev,
                      ),
    comtec_filename = device('refsans.detector.ComtecFilename',
                       description = 'Comtec P7888 Fast System: Filename',
                       tacodevice = '%s/detector' % tacodev,
                      ),
    comtec_image = device('refsans.detector.NullImage',
                                description = "Null image",
                                ),
    comtec = device('devices.generic.Detector',
                        description = "detector, joining all channels",
                        timers = ['comtec_timer'],
                        images = ['comtec_image'],
                        #~ counters = ['fastctr_%c'%c for c in 'abcdefgh'],
                        others = ['comtec_filename'],
                        ),
)

startupcode = '''
SetDetectors(comtec)
'''
