description = 'Shutter and attenuators via Pilz box'

group = 'basic'

includes = []

nethost= 'pgaasrv.pgaa.frm2'

devices = dict(

    shutter = device('pgaa.pilz.Shutter',
                     description = 'secondary experiment shutter',
                     tacodevice = '//%s/pgaa/pilz/shutter' % (nethost,),
                     readback = '//%s/pgaa/pilz/ishutter' % (nethost,),
                     error = '//%s/pgaa/pilz/eshutter' % (nethost,),
                     remote = '//%s/pgaa/pilz/erc' % (nethost,),
                     mapping = {'closed': 2, 'open': 1},
                     maxage = 5,
                     pollinterval = 2,
                     timeout = 3,
                    ),

    att1 = device('pgaa.pilz.Switch',
                  description = 'attenuator 1',
                  tacodevice = '//%s/pgaa/pilz/satt1' % (nethost,),
                  error = '//%s/pgaa/pilz/eatt1' % (nethost,),
                  readback = '//%s/pgaa/pilz/iatt1' % (nethost,),
                  remote = '//%s/pgaa/pilz/erc' % (nethost,),
                  mapping = {'out': 0, 'in': 1},
                  maxage = 5,
                  pollinterval = 2,
                  timeout = 3,
                 ),

    att2 = device('pgaa.pilz.Switch',
                  description = 'attenuator 2',
                  tacodevice = '//%s/pgaa/pilz/satt2' % (nethost,),
                  error = '//%s/pgaa/pilz/eatt2' % (nethost,),
                  readback = '//%s/pgaa/pilz/iatt2' % (nethost,),
                  remote = '//%s/pgaa/pilz/erc' % (nethost,),
                  mapping = {'out': 0, 'in': 1},
                  maxage = 5,
                  pollinterval = 2,
                  timeout = 3,
                 ),

    att3 = device('pgaa.pilz.Switch',
                  description = 'attenuator 3',
                  tacodevice = '//%s/pgaa/pilz/satt3' % (nethost,),
                  error = '//%s/pgaa/pilz/eatt3' % (nethost,),
                  readback = '//%s/pgaa/pilz/iatt3' % (nethost,),
                  remote = '//%s/pgaa/pilz/erc' % (nethost,),
                  mapping = {'out': 0, 'in': 1},
                  maxage = 5,
                  pollinterval = 2,
                  timeout = 3,
                 ),
)
