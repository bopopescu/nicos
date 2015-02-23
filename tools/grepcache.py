#!/usr/bin/env python
#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2015 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""
Small utility to grep within cache files.
"""

import os
import re
import sys
import time
import optparse


def printline(fn, line, opts):
    key, ts, _, val = line.split('\t', 3)
    ts = float(ts)
    val = val.strip()
    if opts.table:
        print '%s\t%s' % (ts, val)
    elif opts.timestamp:
        print '%s: %.3f %s %s' % (fn, ts, key, val)
    else:
        fmtts = time.strftime('%Y-%m-%d %H:%M:%S.%%03d',
                              time.localtime(ts)) % ((ts % 1) * 1000)
        print '%-30s %-25s %-15s %s' % (fn, fmtts, key, val)


def grep(fn, rex, opts):
    with open(fn) as fp:
        fn += ':'
        for line in fp:
            if line.startswith('#'):
                continue
            if rex.search(line):
                printline(fn, line, opts)


def rgrep(dev, dt, rex, opts):
    j = os.path.join
    os.chdir(opts.cachedir)
    for devdir in sorted(os.listdir('.')):
        if devdir == 'lastday' or not os.path.isdir(devdir) or devdir.isdigit():
            continue
        if dev.search(devdir):
            for yeardir in sorted(os.listdir(devdir)):
                for dayfile in sorted(os.listdir(j(devdir, yeardir))):
                    if dt.search('%s-%s' % (yeardir, dayfile)):
                        grep(j(devdir, yeardir, dayfile), rex, opts)


def main():
    parser = optparse.OptionParser(usage='''\
%prog [options] device datetime searchterm

All of "device", "datetime" and "searchterm" are regular expressions.

    * "device" is matched against the NICOS device name of the cache files.
    * "datetime" is matched against the date/time of the cache files,
      in format YYYY-MM-DD.
    * "searchterm" is matched against entries in the cache file.

Hint: to select everything for one argument, use . as argument.''')
    parser.add_option('-d', '--cache-dir', dest='cachedir', default='/data/cache',
                      help='root location of cache database (default /data/cache)')
    parser.add_option('-t', '--timestamp', dest='timestamp', action='store_true',
                      help='output raw timestamp instead of formatted time')
    parser.add_option('-b', '--table', dest='table', action='store_true',
                      help='output timestamp and value suitable for reading in '
                      'with another program')
    opts, args = parser.parse_args()

    # special case for running from checkout
    if opts.cachedir == '/data/cache' and not os.path.isdir(opts.cachedir) \
       and os.path.isdir('data/cache'):
        opts.cachedir = 'data/cache'

    try:
        device, day, searchterm = args
    except ValueError:
        parser.print_usage()
        return 1

    rgrep(re.compile(device, re.I),
          re.compile(day),
          re.compile(searchterm), opts)


sys.exit(main())
