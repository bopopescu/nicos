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
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""Generic device classes using hardware-specific attached devices."""

__version__ = "$Revision$"

from nicos import session
from nicos.core import Device, Param, ConfigurationError


class NoDevice(object):

    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        raise ConfigurationError('proxy %r does not point to any device' % self.name)

    def __setattr__(self, name, value):
        if name != 'name':
            raise ConfigurationError('proxy %r does not point to any device' % self.name)
        object.__setattr__(self, name, value)


class DeviceProxy(Device):
    """
    Generic "proxy" device that can point all access to any other NICOS device.

    The device that should be accessed is set using the "proxy" parameter, which
    can be configured and changed at runtime.  For example, with a DeviceProxy
    instance *T*::

        T.proxy = Tcryo
        read(T)   # will read Tcryo
        T.proxy = Toven
        read(T)   # will read Toven

    This allows to call e.g. the sample temperature by the same name in all
    sample environment setups, but behind the scenes implement it using
    different actual hardware devices.

    If the "proxy" parameter is empty, the proxy points to a special "NoDevice"
    object that raises a :exc:`ConfigurationError` on every access.
    """

    parameters = {
        'proxy':  Param('Device to proxy', type=str, settable=True),
    }

    _ownattrs = ['_obj', '_mode', 'proxy']
    _initialized = False

    def doUpdateProxy(self, devname):
        if not devname:
            self._obj = NoDevice(str(self))
        else:
            self._obj = session.getDevice(devname)

    def __init__(self, name , **config):
        self._obj = None
        Device.__init__(self, name, **config)
        self._initialized = True

    # these methods must not be proxied

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    # generic proxying of missing attributes to the object

    def __getattr__(self, name):
        if not self._initialized:
            raise AttributeError(name)
        else:
            return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in DeviceProxy._ownattrs or not self._initialized:
            object.__setattr__(self, name, value)
        else:
            setattr(self._obj, name, value)

    def __delattr__(self, name):
        if name in DeviceProxy._ownattrs or not self._initialized:
            object.__delattr__(self, name)
        else:
            delattr(self._obj, name)


# proxying of special methods to the object

def make_method(name):
    def method(self, *args, **kw):
        return getattr(self._obj, name)(*args, **kw)
    return method

for name in [
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
        '__float__', '__floordiv__', '__ge__', '__getitem__',
        '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
        '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__',
        '__imul__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__',
        '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__',
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__',
        '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__',
        '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__',
        '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__',
        '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__',
        '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__',
        '__truediv__', '__xor__', 'next',
    ]:
    if hasattr(Device, name):
        setattr(DeviceProxy, name, make_method(name))
