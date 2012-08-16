#  -*- coding: utf-8 -*-

description = 'setup for the cache server'
group = 'special'

devices = dict(
    DB      = device('nicos.cache.server.FlatfileCacheDatabase',
                    storepath = '/data/cache'),

    Server = device('nicos.cache.server.CacheServer',
                    db = 'DB',
                    server = 'pumahw.puma.frm2',
                    loglevel = 'info'),
)
