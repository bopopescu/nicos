#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2019 by the NICOS contributors (see AUTHORS)
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
#   Georg Brandl <g.brandl@fz-juelich.de>
#
# *****************************************************************************

"""Helpers for the "instrument config" dialog."""

from __future__ import absolute_import, division, print_function

import os

from nicos import config


def _get_instr_config():
    currentfile = os.path.join(config.setup_package_path, config.instrument,
                               'setups', 'current_%s.py' % config.instrument)
    return open(currentfile).read()


def _apply_instr_config(code):
    currentfile = os.path.join(config.setup_package_path, config.instrument,
                               'setups', 'current_%s.py' % config.instrument)
    tmpfile = currentfile + '.tmp'
    open(tmpfile, 'w').write(code)
    os.rename(tmpfile, currentfile)
