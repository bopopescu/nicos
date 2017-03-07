description = 'Helios 3He analyzer system'
group = 'optional'

devices = {
    'flipper_%s' % setupname : device('frm2.helios.HePolarizer',
                   description = 'polarization direction of Helios cell with RF flipper',
                   tangodevice = 'tango://%s:10000/box/helios/flipper' % setupname
                  ),
}