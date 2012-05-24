#!/usr/bin/env python
#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
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
#   Björn Pedersen <bjoern.pedersen@frm2.tum.de>
#
# *****************************************************************************

import os
import re
from os import path

from test.utils import raises
from test.scriptSessionTest import ScriptSessionTest


def test_simple():
    code = 'print "Test"'
    setup = 'startup'
    session = ScriptSessionTest('TestScriptSession')
    session.run(setup, code)

def test_raise_simple():
    code = 'raise Exception("testing")'
    setup = 'startup'
    session = ScriptSessionTest('TestScriptSession')
    assert raises(Exception, session.run, setup, code)

def assertRaises(exception, func, *args):
    assert raises(exception, func, *args)

def test_scripts():
    '''test generator executing succesful scripts

    All scripts not containing 'Raises' in their name are considered
    'successful'.
    '''
    testscriptspath = path.join(path.dirname(__file__), 'scripts')
    allscripts = []
    matcher = re.compile('.*Raises(.*)\..*')
    for root, _dirs, files in os.walk(testscriptspath):
        allscripts += [path.join(root, f) for f in files]
    session = ScriptSessionTest('TestScriptSession')
    setup = 'startup'
    for fn in allscripts:
        with open(fn) as codefile:
            code = codefile.read()
        m = matcher.match(fn)
        if m:
            yield assertRaises, Exception, session.run, setup, code
        else:
            yield session.run, setup, code
