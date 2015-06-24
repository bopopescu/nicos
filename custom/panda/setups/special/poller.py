description = 'setup for the poller'

group = 'special'

includes = []

sysconfig = dict(
    cache = 'phys.panda.frm2'
)

devices = dict(
    Poller = device('services.poller.Poller',
                    loglevel = 'info',
                    autosetup = True,
                    alwayspoll = ['water'],
                    neverpoll = ['blenden'],
                    blacklist = ['ss1', 'ss2'],
                    ),
)
