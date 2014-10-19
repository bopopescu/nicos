#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
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

"""Base device classes for usage in NICOS."""

import sys
import types
import inspect
import re
from time import time as currenttime, sleep

from nicos import session
from nicos.core import status
from nicos.core.constants import MASTER, SIMULATION, SLAVE, MAINTENANCE
from nicos.core.utils import formatStatus, getExecutingUser, checkUserLevel, \
    waitForStatus, multiWait, multiStop, multiStatus
from nicos.core.params import Param, Override, Value, floatrange, oneof, \
    anytype, none_or, limits, dictof, listof, tupleof, nicosdev, Attach
from nicos.core.errors import NicosError, ConfigurationError, \
    ProgrammingError, UsageError, LimitError, ModeError, \
    CommunicationError, CacheLockError, InvalidValueError, AccessError
from nicos.utils import loggers, getVersions, parseDateString
from nicos.pycompat import reraise, add_metaclass, itervalues, iteritems, \
    string_types


def usermethod(func):
    """Decorator that marks a method as a user-visible method.

    The method will be shown to the user in the help for a device.
    """
    func.is_usermethod = True
    return func


def requires(**access):
    """Decorator to implement user access control.

    The access is checked based on the keywords given.  Currently, the
    keywords with meaning are:

    * ``'level'``: gives the minimum required user access level and can
      have the values ``GUEST``, ``USER`` or ``ADMIN`` as defined in the
      :mod:`nicos.core.utils` module.
    * ``'mode'``: gives the required exection mode ("master", "slave",
      "maintenance", "simulation").
    * ``'passcode'``: only usable in the interactive console: gives a
      passcode that the user has to type back.

    A special keyword is ``'helpmsg'``; if the access check fails, this gives
    a message that is appended to the error message.

    The wrapper function calls `.Session.checkAccess` to verify the
    requirements.  If the check fails, `.AccessError` is raised.
    """
    def decorator(func):
        def new_func(*args, **kwds):
            try:
                session.checkAccess(access)
            except AccessError as err:
                msg = 'cannot do %s: %s' % (func.__name__, err)
                if 'helpmsg' in access:
                    msg += ' (%s)' % access['helpmsg']
                if args and isinstance(args[0], Device):
                    raise AccessError(args[0], msg)
                raise AccessError(msg)
            return func(*args, **kwds)
        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__
        new_func.real_func = func
        return new_func
    return decorator


class DeviceMixinMeta(type):
    """
    This class provides the __instancecheck__ method for non-Device derived
    mixins.
    """
    def __instancecheck__(cls, inst):  # pylint: disable=C0203
        if inst.__class__ == DeviceAlias and inst._initialized:
            if isinstance(inst._obj, NoDevice):
                return issubclass(inst._cls, cls)
            return isinstance(inst._obj, cls)
        # does not work with Python 2.6!
        # return type.__instancecheck__(cls, inst)
        return issubclass(inst.__class__, cls)


@add_metaclass(DeviceMixinMeta)
class DeviceMixinBase(object):
    """
    Base class for all NICOS device mixin classes not derived from `Device`.

    This class sets the correct metaclass and is easier to use than setting the
    metaclass on each mixin class.  Mixins **must** derive from this class.
    """


class DeviceMeta(DeviceMixinMeta):
    """
    A metaclass that automatically adds properties for the class' parameters,
    and determines a list of user methods ("commands").

    It also merges attached_devices, parameters and parameter_overrides defined
    in the class with those defined in all base classes.
    """

    def __new__(mcs, name, bases, attrs):  # @NoSelf
        if 'parameters' in attrs:
            for pinfo in itervalues(attrs['parameters']):
                pinfo.classname = attrs['__module__'] + '.' + name
        for base in bases:
            if hasattr(base, 'parameters'):
                for pinfo in itervalues(base.parameters):
                    if pinfo.classname is None:
                        pinfo.classname = base.__module__ + '.' + base.__name__
        newtype = type.__new__(mcs, name, bases, attrs)
        # to debug MRO problems you could use this line
        # print 'MRO:', newtype, newtype.mro()
        for entry in newtype.__mergedattrs__:
            newentry = {}
            for base in reversed(bases):
                if hasattr(base, entry):
                    newentry.update(getattr(base, entry))
            newentry.update(attrs.get(entry, {}))
            setattr(newtype, entry, newentry)
        for adevname, entry in newtype.attached_devices.items():
            # adev names are always lowercased
            if adevname != adevname.lower():
                raise ProgrammingError('%r device: attached device name %r is '
                                       'not all-lowercase' % (name, adevname))
            # backwards compatibility: convert all entries to Attach objects
            if not isinstance(entry, Attach):
                _multiple = isinstance(entry[0], list)
                _devclass = entry[0][0] if _multiple else entry[0]
                newtype.attached_devices[adevname] = \
                    Attach(entry[1], _devclass, multiple=_multiple)
        for param, info in iteritems(newtype.parameters):
            # parameter names are always lowercased (enforce this)
            if param != param.lower():
                raise ProgrammingError('%r device: parameter name %r is not '
                                       'all-lowercase' % (name, param))
            if not isinstance(info, Param):
                raise ProgrammingError('%r device %r parameter info should be '
                                       'a Param object' % (name, param))

            # process overrides
            override = newtype.parameter_overrides.get(param)
            if override:
                info = newtype.parameters[param] = override.apply(info)

            # create the getter method
            if not info.volatile:
                def getter(self, param=param):
                    if param not in self._params:
                        self._initParam(param)
                    if self._cache and param != 'name':  # no renaming !
                        value = self._cache.get(self, param, Ellipsis)
                        if value is not Ellipsis:
                            self._params[param] = value
                            return value
                    return self._params[param]
            else:
                rmethod = getattr(newtype, 'doRead' + param.title(), None)
                if rmethod is None:
                    raise ProgrammingError('%r device %r parameter is marked '
                                           'as "volatile=True", but has no '
                                           'doRead%s method' %
                                           (name, param, param.title()))

                def getter(self, param=param, rmethod=rmethod):
                    if self._mode == SIMULATION:
                        return self._initParam(param)
                    value = rmethod(self)
                    if value == self._params[param]:
                        return value
                    if self._cache:
                        self._cache.put(self, param, value)
                    self._params[param] = value
                    return value

            # create the setter method
            if not info.settable:
                def setter(self, value, param=param):
                    raise ConfigurationError(
                        self, 'the %s parameter can only be changed in the '
                        'setup file' % param)
            else:
                wmethod = getattr(newtype, 'doWrite' + param.title(), None)
                umethod = getattr(newtype, 'doUpdate' + param.title(), None)

                def setter(self, value, param=param, wmethod=wmethod,
                           umethod=umethod, chatty=info.chatty):
                    value = self._validateType(value, param)
                    if self._mode == SLAVE:
                        raise ModeError('setting parameter %s not possible in '
                                        'slave mode' % param)
                    elif self._mode == SIMULATION:
                        if umethod:
                            umethod(self, value)
                        if chatty:
                            oldvalue = self._params[param]
                            self.log.info('%s set to %r (was %r)' %
                                          (param, value, oldvalue))
                        self._params[param] = value
                        return
                    oldvalue = getattr(self, param)
                    if wmethod:
                        # allow doWrite to override the value
                        rv = wmethod(self, value)
                        if rv is not None:
                            value = rv
                    if umethod:
                        umethod(self, value)
                    if chatty:
                        self.log.info('%s set to %r (was %r)' % (param, value,
                                                                 oldvalue))
                    self._params[param] = value
                    if self._cache:
                        self._cache.put(self, param, value)

            # create a property and attach to the new device class
            setattr(newtype, param,
                    property(getter, setter, doc=info.formatDoc()))
        del newtype.parameter_overrides
        if 'parameter_overrides' in attrs:
            del attrs['parameter_overrides']
        if 'valuetype' in attrs:
            newtype.valuetype = staticmethod(attrs['valuetype'])

        newtype.commands = {}
        for methname in attrs:
            if methname.startswith(('_', 'do')):
                continue
            method = getattr(newtype, methname)
            if not isinstance(method, types.MethodType):
                continue
            if not hasattr(method, 'is_usermethod'):
                continue
            argspec = inspect.getargspec(method)
            if argspec[0] and argspec[0][0] == 'self':
                del argspec[0][0]  # get rid of "self"
            args = inspect.formatargspec(*argspec)
            if method.__doc__:
                docline = method.__doc__.strip().splitlines()[0]
            else:
                docline = ''
            newtype.commands[methname] = (args, docline)

        return newtype


@add_metaclass(DeviceMeta)
class Device(object):
    """
    An object that has a list of parameters that are read from the configuration
    and have default values.

    Subclasses *can* implement:

    * doPreinit()
    * doInit()
    * doShutdown()
    * doVersion()
    """

    __mergedattrs__ = ['parameters', 'parameter_overrides', 'attached_devices']

    # A dictionary mapping device names to classes (or lists of classes) that
    # describe this device's attached (subordinate) devices.
    attached_devices = {}

    # A dictionary mapping parameter names to parameter descriptions, given as
    # Param objects.
    parameters = {
        'name':        Param('The name of the device', type=str, settable=False,
                             userparam=False),
        'classes':     Param('Names of device class and all its base classes',
                             type=listof(str), settable=False, userparam=False),
        'description': Param('A description of the device', type=str,
                             settable=True),
        'lowlevel':    Param('Whether the device is not interesting to users',
                             type=bool, default=False, userparam=False),
        # Pseudo levels 'input', 'output', and 'action' not included
        'loglevel':    Param('The logging level of the device',
                             type=oneof('debug', 'info', 'warning', 'error'),
                             default='info', settable=True, preinit=True),
    }

    _ownparams = set(['name'])

    # A dictionary mapping parameter names to Override objects that override
    # specific properties of parameters found in base classes.
    parameter_overrides = {}

    # Set this to True on devices that are only created for a time, and whose
    # name can be reused.
    temporary = False

    def __init__(self, name, **config):
        # register self in device registry
        if not self.temporary:
            if name in session.devices:
                raise ProgrammingError('device with name %s already exists' % name)
            session.devices[name] = self

        self._name = name
        # _config: device configuration (all parameter names lower-case)
        self._config = dict((name.lower(), value)
                            for (name, value) in config.items())
        # _params: parameter values from config
        self._params = {'name': name}
        # _infoparams: cached list of parameters to get on info()
        self._infoparams = []
        # _adevs: "attached" device instances
        self._adevs = {}
        # superdevs: reverse adevs for dependency tracking
        self._sdevs = set()
        # execution mode
        self._mode = session.mode

        # initialize a logger for the device
        self.__dict__['log'] = session.getLogger(name)

        try:
            # initialize device
            self.init()
        except:  # really *all* exceptions # pylint: disable=W0702
            t, v, tb = sys.exc_info()
            try:
                self.shutdown()
            except Exception:
                self.log.warning('could not shutdown after creation failed',
                                 exc=1)
            reraise(t, v, tb)

    def __setattr__(self, name, value):
        # disallow modification of public attributes that are not parameters
        if name not in dir(self.__class__) and name[0] != '_' and \
           not name.startswith('print'):
            raise UsageError(self, 'device has no parameter %s, use '
                             'ListParams(%s) to show all' % (name, self))
        else:
            object.__setattr__(self, name, value)

    def __str__(self):
        return self._name

    def __repr__(self):
        if not self.description:
            return '<device %s (a %s.%s)>' % (self._name,
                                              self.__class__.__module__,
                                              self.__class__.__name__)
        return '<device %s "%s" (a %s.%s)>' % (self._name,
                                               self.description,
                                               self.__class__.__module__,
                                               self.__class__.__name__)

    def __reduce__(self):
        # Used for pickling the device e.g. when sending between daemon and GUI
        return (str, (self._name,))

    def getPar(self, name):
        """Get a parameter of the device."""
        if name.lower() not in self.parameters:
            raise UsageError(self, 'device has no parameter %s, use '
                             'ListParams(%s) to show all' % (name, self))
        return getattr(self, name.lower())

    def setPar(self, name, value):
        """Set a parameter of the device to a new value."""
        if name.lower() not in self.parameters:
            raise UsageError(self, 'device has no parameter %s, use '
                             'ListParams(%s) to show all' % (name, self))
        setattr(self, name.lower(), value)

    def doReadName(self):
        return self._name

    def doReadClasses(self):
        return [c.__module__ + '.' + c.__name__ for c in self.__class__.__mro__]

    def doUpdateLoglevel(self, value):
        if session.sessiontype == 'poller':
            # suppress debug/info messages from ordinary devices in the poller
            self.log.setLevel(loggers.WARNING)
        else:
            self.log.setLevel(loggers.loglevels[value])

    def _attachDevices(self):
        """Validate and create attached devices."""
        for aname, entry in sorted(iteritems(self.attached_devices)):
            if not isinstance(entry, Attach):
                raise ProgrammingError(self, 'attached device entry for %r is '
                                       'invalid; the value should be a '
                                       'nicos.core.Attach object' % aname)
            value = self._config.pop(aname, None)
            devlist = []
            class_needed = entry.devclass
            if self._mode == SIMULATION:
                # need to relax this instance check for simulation mode; aliases are
                # not yet set correctly when the devices are created
                class_needed = object
            for i, devname in enumerate(entry.check(self, aname, value)):
                dev = None
                if devname is not None:
                    try:
                        dev = session.getDevice(devname, class_needed, source=self)
                    except UsageError:
                        raise ConfigurationError(
                            self, 'device %r item %d has wrong type (should be %s)' %
                            (aname, i + 1, entry.devclass.__name__))
                    dev._sdevs.add(self._name)
                devlist.append(dev)
            self._adevs[aname] = devlist[0] if entry.single else devlist

    def init(self):
        """Initialize the object; this is called by the NICOS system when the
        device instance has been created.

        This method first initializes all attached devices (creating them if
        necessary), then initializes parameters.

        .. XXX expand parameter init procedure

        .. method:: doPreinit(mode)

           This method, if present, is called before parameters are initialized
           (except for parameters that have the ``preinit`` property set to
           true).

           This allows to initialize a hardware connection if it is necessary
           for the various ``doRead...()`` methods of other parameters that read
           the current parameter value from the hardware.

        .. method:: doInit(mode)

           This method, if present, is called after all parameters have been
           initialized.  It is the correct place to set up additional
           attributes, or to perform initial (read-only!) communication with the
           hardware.

        .. note:: ``doPreinit()`` and ``doInit()`` are called regardless of the
           current execution mode.  This means that if one of these methods does
           hardware access, it must be done only if ``mode != SIMULATION``.
        """
        self._cache = None
        self._subscriptions = []

        self._attachDevices()

        self._cache = self._getCache()
        lastconfig = None
        if self._cache:
            lastconfig = self._cache.get('_lastconfig_', self._name, None)
            old_classes = self._cache.get(self, 'classes')
            if old_classes and old_classes != self.doReadClasses():
                # This commented code leads to problems if the same device is
                # defined in the startup setup and the final loaded setup, e.g.
                # for the Sample device
                # self.log.warning('device changed class, clearing all cached '
                #                 'parameter values')
                # self._cache.clear(self)
                pass

        def _init_param(param, paraminfo):
            param = param.lower()
            # mandatory parameters must be in config, regardless of cache
            if paraminfo.mandatory and param not in self._config:
                raise ConfigurationError(self, 'missing configuration '
                                         'parameter %r' % param)
            # try to get from cache
            value = Ellipsis  # Ellipsis representing "no value" since None
                              # is a valid value for some parameters
            if self._cache:
                value = self._cache.get(self, param, Ellipsis)
                if param == 'name':  # clean up legacy, wrong values
                    self._cache.put(self, 'name', self._name)
                    value = self._name
            if value is not Ellipsis:
                value = self._validateType(value, param, paraminfo)
                if param in self._ownparams:
                    self._params[param] = value
                    return
                if param in self._config:
                    cfgvalue = self._config[param]
                    if cfgvalue != value:
                        prefercache = paraminfo.prefercache
                        if prefercache is None:
                            prefercache = paraminfo.settable
                        if lastconfig and lastconfig.get(param) != cfgvalue:
                            self.log.warning(
                                'value of %s from cache (%r) differs from '
                                'configured value (%r), using configured '
                                'since it was changed in the setup file' %
                                (param, value, cfgvalue))
                            value = self._validateType(cfgvalue, param, paraminfo)
                            self._cache.put(self, param, value)
                        elif prefercache:
                            self.log.warning(
                                'value of %s from cache (%r) differs from '
                                'configured value (%r), using cached' %
                                (param, value, cfgvalue))
                        else:
                            self.log.warning(
                                'value of %s from cache (%r) differs from '
                                'configured value (%r), using configured' %
                                (param, value, cfgvalue))
                            value = self._validateType(cfgvalue, param, paraminfo)
                            self._cache.put(self, param, value)
                umethod = getattr(self, 'doUpdate' + param.title(), None)
                if umethod:
                    umethod(value)
                self._params[param] = value
            else:
                self._initParam(param, paraminfo)
                notfromcache.append(param)
            if paraminfo.category is not None:
                self._infoparams.append((paraminfo.category, param,
                                         paraminfo.unit))
            # end of _init_param()

        notfromcache = []
        later = []

        for param, paraminfo in iteritems(self.parameters):
            if paraminfo.preinit:
                _init_param(param, paraminfo)
            else:
                later.append((param, paraminfo))

        if hasattr(self, 'doPreinit'):
            self.doPreinit(self._mode)

        for param, paraminfo in later:
            _init_param(param, paraminfo)

        # warn about parameters that weren't present in cache
        if self._cache and notfromcache:
            self.log.info('these parameters were not present in cache: ' +
                          ', '.join(notfromcache))

        self._infoparams.sort()

        # subscribe to parameter value updates, if a doUpdate method exists
        if self._cache:
            for param in self.parameters:
                umethod = getattr(self, 'doUpdate' + param.title(), None)
                if umethod:
                    def updateparam(key, value, time, umethod=umethod):
                        umethod(value)
                    self._cache.addCallback(self, param, updateparam)
                    self._subscriptions.append((param, updateparam))

        if self._cache:
            self._cache.put('_lastconfig_', self._name, self._config)

        # call custom initialization
        if hasattr(self, 'doInit'):
            self.doInit(self._mode)

    def _getCache(self):
        """Indirection needed by the Cache client itself."""
        return session.cache

    def _validateType(self, value, param, paraminfo=None):
        """Validate and coerce the value of a parameter to the correct type.

        If the value can't be coerced, a ConfigurationError is raised.
        """
        paraminfo = paraminfo or self.parameters[param]
        try:
            value = paraminfo.type(value)
        except (ValueError, TypeError) as err:
            raise ConfigurationError(self, '%r is an invalid value for '
                                     'parameter %s: %s' % (value, param, err))
        return value

    def _initParam(self, param, paraminfo=None):
        """Get an initial value for the parameter, called when the cache
        doesn't contain such a value.

        If present, a doReadParam method is called.  Otherwise, the value comes
        from either the setup file or the device-specific default value.
        """
        paraminfo = paraminfo or self.parameters[param]
        rmethod = getattr(self, 'doRead' + param.title(), None)
        umethod = getattr(self, 'doUpdate' + param.title(), None)
        done = False
        # try to read from the hardware (only in non-simulation mode)
        if self._mode != SIMULATION and rmethod:
            try:
                value = rmethod()
            except NicosError:
                self.log.warning('could not read initial value for parameter '
                                 '%s from device' % param)
            else:
                done = True
        if not done and param in self._params:
            # happens when called from a param getter, not from init()
            value = self._params[param]
        elif not done:
            value = self._config.get(param, paraminfo.default)
        value = self._validateType(value, param, paraminfo)
        if self._cache:  # will not be there in simulation mode
            self._cache.put(self, param, value)
        # always call update methods, they should be working for simulation
        if umethod:
            umethod(value)
        self._params[param] = value
        return value

    def _setROParam(self, param, value):
        """Set an otherwise read-only parameter.

        This is useful for parameters that change at runtime, but indirectly,
        such as "last filenumber".
        """
        value = self._validateType(value, param)
        self._params[param] = value
        if self._cache:
            self._cache.put(self, param, value)

    def _setMode(self, mode):
        """Set a new execution mode."""
        self._mode = mode
        if mode == SIMULATION:
            # switching to simulation mode: remove cache entirely
            # and rely on saved _params and values
            self._cache = None

    def history(self, name='value', fromtime=None, totime=None):
        """Return a history of the parameter *name* (can also be ``'value'`` or
        ``'status'``).

        *fromtime* and *totime* can be used to limit the time window.  They can
        be:

        * positive numbers: interpreted as UNIX timestamps
        * negative numbers: interpreted as hours back from now
        * strings: in one of the formats 'HH:MM', 'HH:MM:SS',
          'YYYY-MM-DD', 'YYYY-MM-DD HH:MM' or 'YYYY-MM-DD HH:MM:SS'

        Default is to query the values of the last hour.
        """
        if not self._cache:
            # no cache is configured for this setup
            return []
        else:
            if fromtime is None:
                fromtime = -1
            if isinstance(fromtime, string_types):
                fromtime = parseDateString(fromtime)
            elif fromtime < 0:
                fromtime = currenttime() + fromtime * 3600
            if totime is None:
                totime = currenttime()
            elif isinstance(totime, string_types):
                totime = parseDateString(totime, enddate=True)
            elif totime < 0:
                totime = currenttime() + totime * 3600
            return self._cache.history(self, name, fromtime, totime)

    def info(self):
        """Return "device information" as an iterable of tuples ``(category,
        name, value)``.

        This "device information" is put into data files and should therefore
        include any parameters that will be essential to record the current
        status of the instrument.

        The default implementation already collects all parameters whose
        ``category`` property is set.

        .. method:: doInfo()

           This method can add more device information by returning it as a
           sequence of tuples.
        """
        if hasattr(self, 'doInfo'):
            for item in self.doInfo():
                yield item
        selfunit = getattr(self, 'unit', '')
        for category, name, unit in self._infoparams:
            try:
                parvalue = getattr(self, name)
            except Exception as err:
                self.log.warning('error getting %s parameter for info()' %
                                 name, exc=err)
                continue
            parunit = (unit or '').replace('main', selfunit)
            yield (category, name, '%s %s' % (parvalue, parunit))

    def shutdown(self):
        """Shut down the device.  This method is called by the NICOS system when
        the device is destroyed, manually or because the current setup is
        unloaded.

        .. method:: doShutdown()

           This method is called, if present, but not in simulation mode.  It
           should perform cleanup, for example closing connections to hardware.
        """
        self.log.debug('shutting down device')
        caughtExc = None
        if self._mode != SIMULATION:
            # do not execute shutdown actions when simulating

            # remove subscriptions to parameter value updates
            if self._cache:
                for param, func in self._subscriptions:
                    self._cache.removeCallback(self, param, func)

            # execute custom shutdown actions
            if hasattr(self, 'doShutdown'):
                try:
                    self.doShutdown()
                except Exception:
                    caughtExc = sys.exc_info()

        for adev in self._adevs.values():
            if isinstance(adev, list):
                for real_adev in adev:
                    real_adev._sdevs.discard(self._name)
            elif adev is not None:
                adev._sdevs.discard(self._name)
        session.devices.pop(self._name, None)
        session.explicit_devices.discard(self._name)
        # re-raise the doShutdown error
        if caughtExc is not None:
            reraise(*caughtExc)

    @usermethod
    def version(self):
        """Return a list of versions for this device.

        These are tuples (component, version) where a "component" can be the
        name of a Python module, or an external dependency (like a TACO server).

        The base implementation already collects VCS revision information
        available from all Python modules involved in the class inheritance
        chain of the device class.

        .. method:: doVersion()

           This method is called if present, and should return a list of
           (component, version) tuples that are added to the version info.
        """
        versions = getVersions(self)
        if hasattr(self, 'doVersion'):
            versions.extend(self.doVersion())
        return versions

    def _cachelock_acquire(self, timeout=3):
        """Acquire an exclusive lock for using this device from the cache.  This
        can be used if read access to the device needs to be locked (write
        access is locked anyway, since only one NICOS session can be the master
        session at a time).
        """
        if not self._cache:
            return
        start = currenttime()
        while True:
            try:
                self._cache.lock(self._name)
            except CacheLockError:
                if currenttime() > start + timeout:
                    raise CommunicationError(self, 'device locked in cache')
                sleep(0.3)
            else:
                break

    def _cachelock_release(self):
        """Release the exclusive cache lock for this device.

        Always use like this::

           self._cachelock_acquire()
           try:
               ...  # do locked operations
           finally:
               self._cachelock_release()
        """
        if not self._cache:
            return
        try:
            self._cache.unlock(self._name)
        except CacheLockError:
            raise CommunicationError(self, 'device locked by other instance')


class AutoDevice(DeviceMixinBase):
    """Abstract mixin for devices that are created automatically as dependent
    devices of other devices.
    """


class Readable(Device):
    """
    Base class for all readable devices.

    Subclasses *need* to implement:

    * doRead()
    * doStatus()

    Subclasses *can* implement:

    * doReset()
    * doPoll()
    * valueInfo()
    """

    # Set this to True on devices that directly access hardware, and therefore
    # should have their actions simulated.
    hardware_access = True

    parameters = {
        'fmtstr':       Param('Format string for the device value', type=str,
                              default='%.3f', settable=True),
        'unit':         Param('Unit of the device main value', type=str,
                              mandatory=True, settable=True),
        'maxage':       Param('Maximum age of cached value and status (zero to '
                              'never use cached values, or None to cache them '
                              'indefinitely)', unit='s', settable=True,
                              type=none_or(floatrange(0, 24 * 3600)), default=6),
        'pollinterval': Param('Polling interval for value and status (or None '
                              'to disable polling)', unit='s', settable=True,
                              type=none_or(floatrange(0.5, 24 * 3600)), default=5),
        'warnlimits':   Param('Range in which the device value should be '
                              'in normal operation; warnings may be triggered '
                              'when it is outside', settable=True, chatty=True,
                              type=none_or(tupleof(anytype, anytype))),
    }

    def init(self):
        self._info_errcount = 0
        self._sim_active = False
        Device.init(self)
        # value in simulation mode
        self._sim_active = self._mode == SIMULATION and self.hardware_access
        self._sim_old_value = None
        self._sim_value = 0  # no way to configure a useful default...
        self._sim_min = None
        self._sim_max = None
        self._sim_started = None
        self._sim_preset = {}

    def _sim_getMinMax(self):
        """Return info about the value range this device had in a simulation.

        The return value is a list of tuples ``(value name, last value, minimum
        value, maximum value)``.  By default this has one entry, where "value
        name" is the device name.
        """
        if self._sim_min is not None:
            return [(self.name, self.format(self._sim_value),
                     self.format(self._sim_min), self.format(self._sim_max))]
        else:
            return []

    def _sim_setValue(self, pos):
        self._sim_old_value = self._sim_value
        self._sim_value = pos
        if self._sim_min is None:
            self._sim_min = pos
        self._sim_min = min(pos, self._sim_min)
        if self._sim_max is None:
            self._sim_max = pos
        self._sim_max = max(pos, self._sim_max)

    def _setMode(self, mode):
        sim_active = mode == SIMULATION and self.hardware_access
        if sim_active:
            # save the last known value
            try:
                self._sim_value = self.read()  # cached value is ok here
                self.log.debug('last value before simulation mode is %r' %
                               (self._sim_value,))
            except Exception as err:
                self.log.warning('error reading last value', exc=err)
        self._sim_active = sim_active
        Device._setMode(self, mode)

    def __call__(self, *values):
        """Allow dev() as shortcut for read."""
        if values:
            # give a nicer error message than "TypeError: takes 1 argument"
            raise UsageError(self, 'not a moveable device')
        return self.read()

    def _get_from_cache(self, name, func, maxage=None):
        """Get *name* from the cache, or call *func* if outdated/not present.

        If the *maxage* parameter is set, do not allow the value to be older
        than that amount of seconds.
        """
        if not self._cache:
            return func()
        val = None
        if 1:  # self.hardware_access:  XXX decide if this should be enabled
            if maxage != 0:
                val = self._cache.get(
                    self, name,
                    mintime=currenttime() - maxage if maxage is not None else 0)
        if val is None:
            val = func(self.maxage if maxage is None else maxage)
            self._cache.put(self, name, val, currenttime(), self.maxage)
        return val

    def valueInfo(self):
        """Describe the values read by this device.

        Return a tuple of :class:`~nicos.core.params.Value` instances describing
        the values that :meth:`read` returns.

        This must be overridden by every Readable that returns more than one
        value in a list.  For example, a slit that returns a width and height
        would define ::

            def valueInfo(self):
                return (Value(self.name + '.width', unit=self.unit),
                        Value(self.name + '.height', unit=self.unit))

        By default, this returns a Value that indicates one return value with
        the proper unit and format string of the device.
        """
        return Value(self.name, unit=self.unit, fmtstr=self.fmtstr),

    @usermethod
    def read(self, maxage=None):
        """Read the (possibly cached) main value of the device.

        .. method:: doRead(maxage=0)

           This method must be implemented to read the actual device value from
           the device.  It is only called if the last cached value is out of
           date, or no cache is available.

           The *maxage* parameter should be given to read() calls of subdevices.
        """
        if self._sim_active:
            return self._sim_value
        return self._get_from_cache('value', self.doRead, maxage)

    @usermethod
    def status(self, maxage=None):
        """Return the (possibly cached) status of the device.

        The status is a tuple of one of the integer constants defined in the
        :mod:`nicos.core.status` module, and textual extended info.

        .. method:: doStatus(maxage=0)

           This method can be implemented to get actual device status from the
           device.  It is only called if the last cached value is out of
           date, or no cache is available.

           If no ``doStatus()`` is implemented, ``status()`` tries to determine
           the status via `nicos.core.utils.multiStatus` of the attached devices.
           If that is not possible, it returns
           ``status.UNKNOWN, 'doStatus not implemented'``.

           The *maxage* parameter should be given to status() calls of
           subdevices.
        """
        if self._sim_active:
            return (status.OK, 'simulated ok')
        try:
            value = self._get_from_cache('status', self.doStatus, maxage)
        except NicosError as err:
            value = (status.ERROR, str(err))
        if value[0] not in status.statuses:
            raise ProgrammingError(self, 'status constant %r is unknown' %
                                   value[0])
        return value

    def doStatus(self, maxage=0):
        if self._adevs:
            return multiStatus(self._adevs, maxage)
        return (status.UNKNOWN, 'doStatus not implemented')

    def poll(self, n=0, maxage=0):
        """Get status and value directly from the device and put both values
        into the cache.  For continuous polling, *n* should increase by one with
        every call to *poll*.

        .. method:: doPoll(n)

           If present, this method is called to perform additional polling,
           e.g. on parameters that can be changed from outside the NICOS system.
           The *n* parameter can be used to perform the polling less frequently
           than the polling of value and status.

           If doPoll returns a (status, value) tuple, they are used instead of
           calling doStatus and doRead again.

        .. automethod:: _pollParam
        """
        if self._sim_active or self._cache is None:
            return (self.status(), self.read())
        ret = None
        if hasattr(self, 'doPoll'):
            try:
                ret = self.doPoll(n)
            except Exception:
                self.log.debug('error in doPoll', exc=1)
        if ret is not None and ret[0] is not None:
            ct = currenttime()
            self._cache.put(self, 'status', ret[0], ct, self.maxage)
            self._cache.put(self, 'value', ret[1], ct, self.maxage)
            return ret[0], ret[1]
        # updates shall always get through to the cache
        self._cache.invalidate(self, 'value')
        self._cache.invalidate(self, 'status')
        return self.status(maxage), self.read(maxage)

    def _pollParam(self, name, with_ttl=0):
        """Read a parameter value from the hardware and put its value into the
        cache.  This is intendend to be used from :meth:`doPoll` methods, so
        that they don't have to implement parameter polling themselves.  If
        *with_ttl* is > 0, the cached value gets the TTL of the device value,
        determined by :attr:`maxage`, multiplied by *with_ttl*.
        """
        value = getattr(self, 'doRead' + name.title())()
        if with_ttl:
            self._cache.put(self, name, value, currenttime(),
                            (self.maxage or 0) * with_ttl)
        else:
            self._cache.put(self, name, value)

    @usermethod
    def reset(self):
        """Reset the device hardware.  Returns the new status afterwards.

        This operation is forbidden in slave mode, and a no-op for hardware
        devices in simulation mode.

        .. method:: doReset()

           This method is called if implemented.  Otherwise, this is a no-op.
        """
        if self._mode == SLAVE:
            raise ModeError('reset not possible in slave mode')
        elif self._sim_active:
            return
        if hasattr(self, 'doReset'):
            self.doReset()
        # make sure, status is propagated to the cache after a reset
        self._cache.invalidate(self, 'status')
        return self.status(0)

    def format(self, value, unit=False):
        """Format a value from :meth:`read` into a human-readable string.

        The device unit is not included unless *unit* is true.

        This is done using Python string formatting (the ``%`` operator) with
        the :attr:`fmtstr` parameter value as the format string.
        """
        if isinstance(value, list):
            value = tuple(value)
        try:
            ret = self.fmtstr % value
        except (TypeError, ValueError):
            ret = str(value)
        if unit and self.unit:
            return ret + ' ' + self.unit
        return ret

    def info(self):
        """Automatically add device main value and status (if not OK)."""
        try:
            val = self.read()
            yield ('general', 'value', self.format(val, unit=True))
        except Exception as err:
            self._info_errcount += 1
            # only display the message for the first 5 times and then
            # every 20 measurements. always display if in debugmode
            if self._info_errcount <= 5 or self._info_errcount % 20 == 0:
                self.log.warning('error reading device for info()', exc=err)
            else:
                self.log.debug('error reading device for info()', exc=err)
            yield ('general', 'value', 'Error: %s' % err)
        else:
            self._info_errcount = 0
        try:
            st = self.status()
        except Exception as err:
            yield ('status', 'status', 'Error: %s' % err)
        else:
            if st[0] not in (status.OK, status.UNKNOWN):
                yield ('status', 'status', formatStatus(st))
        for item in Device.info(self):
            yield item


class Moveable(Readable):
    """
    Base class for moveable devices.

    Subclasses *need* to implement:

    * doStart(value)

    Subclasses *can* implement:

    * doStop()
    * doWait()
    * doIsAllowed()
    * doTime()
    """

    parameters = {
        'target': Param('Last target position of a start() action',
                        unit='main', type=anytype, default=None),
        'fixed':  Param('None if the device is not fixed, else a string '
                        'describing why', settable=False, userparam=False,
                        type=str),
        'fixedby':  Param('Who fixed it?', settable=False, userparam=False,
                          type=none_or(tupleof(str, int)), default=None),
        'requires': Param('Access requirements for moving the device',
                          type=dictof(str, anytype), userparam=False),
    }

    # The type of the device value, used for typechecking in doStart().
    @staticmethod
    def valuetype(value):
        """The type of the device value, used for type checking in doStart().

        This should be a static function as the real function is assigned
        externally from functions defined in nicos.core.params, so no class
        instance need to be passed.
        """
        return value

    valuetype = anytype

    def __call__(self, *pos):
        """Allow dev() and dev(newpos) as shortcuts for read and start."""
        if not pos:
            return self.read()
        # allow tuple values to be spelled as individual items,
        # e.g. slit(1, 2, 3, 4) instead of slit((1, 2, 3, 4))
        if len(pos) == 1:
            return self.start(pos[0])
        return self.start(pos)

    @usermethod
    def isAllowed(self, pos):
        """Check if the given position can be moved to.

        The return value is a tuple ``(valid, why)``.  The first item is a
        boolean indicating if the position is valid, the second item is a string
        with the reason if it is invalid.

        .. method:: doIsAllowed(pos)

           This method must be implemented to check the validity.  If it does
           not exist, all positions are valid.

           Note: to implement ordinary (min, max) limits, do not use this method
           but inherit your device from :class:`HasLimits`.  This takes care of
           all limit processing.
        """
        if hasattr(self, 'doIsAllowed'):
            return self.doIsAllowed(pos)
        return True, ''

    @usermethod
    def start(self, pos):
        """Start movement of the device to a new position.

        This method does not generally wait for completion of the movement,
        although individual devices can implement it that way if it is
        convenient.  In that case, no :meth:`doWait` should be implemented.

        The validity of the given *pos* is checked by calling :meth:`isAllowed`
        before :meth:`doStart` is called.

        This operation is forbidden in slave mode.  In simulation mode, it sets
        an internal variable to the given position for hardware devices instead
        of calling :meth:`doStart`.

        .. method:: doStart(pos)

           This method must be implemented and actually move the device to the
           new position.
        """
        if self._mode == SLAVE:
            raise ModeError(self, 'start not possible in slave mode')
        if self.fixed:
            # try to determine if we are already there
            try:
                # this may raise if the position values are not numbers
                if abs(self.read() - pos) <= getattr(self, 'precision', 0):
                    self.log.debug('device fixed; start() allowed since '
                                   'already at desired position %s' % pos)
                    return
            except Exception:
                pass
            self.log.warning('device fixed, not moving: %s' % self.fixed)
            return
        if self.requires:
            try:
                session.checkAccess(self.requires)
            except AccessError as err:
                raise AccessError(self, 'cannot start device: %s' % err)
        try:
            pos = self.valuetype(pos)
        except (ValueError, TypeError) as err:
            raise InvalidValueError(self, '%r is an invalid value for this '
                                    'device: %s' % (pos, err))
        ok, why = self.isAllowed(pos)
        if not ok:
            raise LimitError(self, 'moving to %s is not allowed: %s' %
                             (self.format(pos, unit=True), why))
        self._setROParam('target', pos)
        if self._sim_active:
            self._sim_setValue(pos)
            self._sim_started = session.clock.time
            return
        if self._cache:
            self._cache.invalidate(self, 'value')
            self._cache.invalidate(self, 'status')
        self.doStart(pos)

    move = start

    @usermethod
    def wait(self):
        """Wait until movement of device is completed.

        Return current device value after waiting.  This is a no-op for hardware
        devices in simulation mode.

        .. method:: doWait()

           This method is called to actually do the waiting.
           It should be implemented in derived classes requiring special
           treatment.
           The default implementation polls the device status until it is no
           longer BUSY, i.e. 'waits' for the device.
           If no :meth:`doStatus` is implemented, :meth:`doWait` may be NOT called
           as those devices are assumed to always move instantaneously!

           Implementation hint: If you correctly implement :meth:`doStatus` and
           your device is not very special, there is no need to implement
           :meth:`doWait()`.
        """
        if self._sim_active:
            time = 0
            if not hasattr(self, 'doTime'):
                if 'speed' in self.parameters and self.speed != 0 and \
                        self._sim_old_value is not None:
                    time = abs(self._sim_value - self._sim_old_value) / \
                        self.speed
                elif 'ramp' in self.parameters and self.ramp != 0 and \
                        self._sim_old_value is not None:
                    time = abs(self._sim_value - self._sim_old_value) / \
                        (self.ramp / 60.)
            elif self._sim_old_value is not None:
                try:
                    time = self.doTime(self._sim_old_value, self._sim_value)
                except Exception:
                    self.log.warning('could not time movement', exc=1)
            if self._sim_started is not None:
                session.clock.wait(self._sim_started + time)
                self._sim_started = None
            self._sim_old_value = self._sim_value
            return self._sim_value
        lastval = None
        try:
            if self.fixed:
                self.log.debug('device fixed, not waiting: %s' % self.fixed)
            elif hasattr(self, 'doStatus'):  # might really wait
                session.beginActionScope('Waiting: %s -> %s' %
                                         (self, self.format(self.target)))
                try:
                    lastval = self.doWait()
                finally:
                    session.endActionScope()
            else:
                if self.__class__.doWait != Moveable.doWait:
                    # legacy case, custom doWait, but no doStatus!!!
                    self.log.warning('Legacywarning: %r has a doWait, but no '
                                     'doStatus, please fix it!' % self.__class__)
                lastval = self.doWait()  # prefer functionality for the moment....
                # no else needed as this is basically a NOP
                # (status returns UNKNOWN, default doWait() returns immediately....)
        finally:
            # update device value in cache and return it
            if lastval is not None:
                # if doWait() returns something, assume it's the latest value
                val = lastval
            else:
                # else, assume the device did move and the cache needs to be
                # updated in most cases
                val = self.doRead(0)  # not read(0), we already cache value below
            if self._cache and self._mode != SLAVE:
                self._cache.put(self, 'value', val, currenttime(), self.maxage)
        return val

    def doWait(self):
        """Wait until movement of device is completed.

        This default implementation is supposed to be overriden in derived
        classes and just waits for all attached devices and then polls the status
        of the device itself until it is not BUSY anymore.  For details how
        this is done, have a look into `nicos.core.utils.multiWait` and
        `nicos.core.utils.waitForStatus`.

        Implementation hint: normally you would only need to override this in
        very special cases as it already handles most cases correctly.
        """
        if self._adevs:
            multiWait(self._adevs)
        waitForStatus(self)

    @usermethod
    def maw(self, target):
        """Move to target and wait for completion.

        Equivalent to ``dev.start(target); return dev.wait()``.
        """
        self.start(target)
        return self.wait()

    @usermethod
    def stop(self):
        """Stop any movement of the device.

        This operation is forbidden in slave mode, and a no-op for hardware
        devices in simulation mode.

        .. method:: doStop()

           This is called to actually stop the device.  If not present,
           :meth:`stop` will try to stop all attached_devices, if any.
           Otherwise this is a no-op.

        The `stop` method will return the device status after stopping.
        """
        if self._mode == SLAVE:
            raise ModeError(self, 'stop not possible in slave mode')
        elif self._sim_active:
            return
        if self.fixed:
            self.log.debug('device fixed, not stopping: %s' % self.fixed)
            return
        if self.requires:
            try:
                session.checkAccess(self.requires)
            except AccessError as err:
                raise AccessError(self, 'cannot stop device: %s' % err)
        if hasattr(self, 'doStop'):
            self.doStop()
        elif self._adevs:
            multiStop(self._adevs)
        if self._cache:
            self._cache.invalidate(self, 'value')
            self._cache.invalidate(self, 'status')

    @usermethod
    def fix(self, reason=''):
        """Fix the device: don't allow movement anymore.

        This blocks :meth:`start` or :meth:`stop` when called on the device.
        """
        eu = getExecutingUser()
        if self.fixedby and not checkUserLevel(self.fixedby[1], eu):
            # fixed and not enough rights
            self.log.error('device was fixed by %r already' % self.fixedby[0])
            return False
        else:
            if self.status()[0] == status.BUSY:
                self.log.warning('device appears to be busy')
            if reason:
                reason += ' (fixed by %r)' % eu.name
            else:
                reason = 'fixed by %r' % eu.name
            self._setROParam('fixed', reason)
            self._setROParam('fixedby', (eu.name, eu.level))
            return True

    @usermethod
    def release(self):
        """Release the device, i.e. undo the effect of fix()."""
        eu = getExecutingUser()
        if self.fixedby and not checkUserLevel(self.fixedby[1], eu):
            # fixed and not enough rights
            self.log.error('device was fixed by %r and you are not allowed '
                           'to release it' % self.fixedby[0])
            return False
        else:
            self._setROParam('fixed', '')
            self._setROParam('fixedby', None)
            return True


class HasLimits(DeviceMixinBase):
    """
    This mixin can be inherited from device classes that are continuously
    moveable.  It automatically adds two parameters, absolute and user limits,
    and overrides :meth:`.isAllowed` to check if the given position is within the
    limits before moving.

    .. note:: In a base class list, ``HasLimits`` must come before ``Moveable``,
       e.g.::

          class MyDevice(HasLimits, Moveable): ...

    The `abslimits` parameter cannot be set after creation of the device and
    must be given in the setup configuration.

    The `userlimits` parameter gives the actual minimum and maximum values
    that the device can be moved to.  The user limits must lie within the
    absolute limits.

    **Important:** If the device is also an instance of `HasOffset`, it should
    be noted that the `abslimits` are in hardware units (disregarding the
    offset), while the `userlimits` are in logical units (taking the offset
    into account).

    The class also provides properties to read or set only one item of the
    limits tuple:

    .. attribute:: absmin
                   absmax

       Getter properties for the first/second value of `abslimits`.

    .. attribute:: usermin
                   usermax

       Getter and setter properties for the first/second value of `userlimits`.

    """

    parameters = {
        'userlimits': Param('User defined limits of device value', unit='main',
                            type=limits, settable=True, chatty=True),
        'abslimits':  Param('Absolute limits of device value', unit='main',
                            type=limits, mandatory=True),
    }

    # By default, something that has limits has a floating (analog) value.
    valuetype = float

    def init(self):
        if isinstance(self, Moveable):
            Moveable.init(self)
        if isinstance(self, HasOffset):
            offset = self.offset
        else:
            offset = 0
        amin, amax = self.absmin - offset, self.absmax - offset
        umin, umax = self.userlimits
        if self._mode == MASTER:
            # re-set user limits to be within absolute limits
            restricted_limits = (max(umin, amin), min(umax, amax))
            if restricted_limits != (umin, umax):
                self.userlimits = restricted_limits
        else:
            if umin < amin:
                self.log.warning('user minimum (%s) below absolute minimum (%s), '
                                 'please check and re-set limits' % (umin, amin))
            if umax > amax:
                self.log.warning('user maximum (%s) above absolute maximum (%s), '
                                 'please check and re-set limits' % (umax, amax))
        if self._mode == SIMULATION:
            # special case: in simulation mode, doReadUserlimits is not called,
            # so the limits are not set from the absolute limits, and are always
            # (0, 0) except when set in the setup file
            if self.userlimits == (0.0, 0.0):
                self.userlimits = self.abslimits

    @property
    def absmin(self):
        return self.abslimits[0]

    @property
    def absmax(self):
        return self.abslimits[1]

    def __getusermin(self):
        return self.userlimits[0]

    def __setusermin(self, value):
        self.userlimits = (value, self.userlimits[1])

    usermin = property(__getusermin, __setusermin)

    def __getusermax(self):
        return self.userlimits[1]

    def __setusermax(self, value):
        self.userlimits = (self.userlimits[0], value)

    usermax = property(__getusermax, __setusermax)

    del __getusermin, __setusermin, __getusermax, __setusermax

    def isAllowed(self, target):
        limits = self.userlimits
        if not limits[0] <= target <= limits[1]:
            return False, 'limits are [%s, %s]' % limits
        if hasattr(self, 'doIsAllowed'):
            return self.doIsAllowed(target)
        return True, ''

    def _checkLimits(self, limits):
        umin, umax = limits
        amin, amax = self.abslimits
        if isinstance(self, HasOffset):
            offset = getattr(self, '_new_offset', self.offset)
            umin += offset
            umax += offset
        else:
            offset = 0
        if umin > umax:
            raise ConfigurationError(
                self, 'user minimum (%s, offset %s) above the user '
                'maximum (%s, offset %s)' % (umin, offset, umax, offset))
        if umin < amin:
            raise ConfigurationError(
                self, 'user minimum (%s, offset %s) below the '
                'absolute minimum (%s)' % (umin, offset, amin))
        if umax > amax:
            raise ConfigurationError(
                self, 'user maximum (%s, offset %s) above the '
                'absolute maximum (%s)' % (umax, offset, amax))

    def doReadUserlimits(self):
        if 'userlimits' not in self._config:
            self.log.info('setting userlimits from abslimits, which are %s'
                          % (self.abslimits,))
            return self.abslimits
        cfglimits = self._config['userlimits']
        self._checkLimits(cfglimits)
        return cfglimits

    def doWriteUserlimits(self, value):
        self._checkLimits(value)
        if isinstance(self, HasOffset) and hasattr(self, '_new_offset'):
            # when changing the offset, the userlimits are adjusted so that the
            # value stays within them, but only after the new offset is applied
            return
        curval = self.read(0)
        if isinstance(self, HasPrecision):
            outoflimits = curval + self.precision < value[0] or \
                curval - self.precision > value[1]
        else:
            outoflimits = not (value[0] <= curval <= value[1])
        if outoflimits:
            self.log.warning('current device value (%s) not within new '
                             'userlimits (%s, %s)' %
                             ((self.format(curval, unit=True),) + value))

    def _adjustLimitsToOffset(self, value, diff):
        """Adjust the user limits to the given offset.

        Used by the HasOffset mixin class to adjust the offset. *value* is the
        offset value, *diff* the offset difference.
        """
        limits = self.userlimits
        self._new_offset = value
        self.userlimits = (limits[0] - diff, limits[1] - diff)
        del self._new_offset


class HasOffset(DeviceMixinBase):
    """
    Mixin class for Readable or Moveable devices that want to provide an
    'offset' parameter and that can be adjusted via adjust().

    This is *not* directly a feature of Moveable, because providing this
    transparently this would mean that `doRead()` returns the un-adjusted value
    while `read()` returns the adjusted value.  It would also mean that the
    un-adjusted value is stored in the cache, which is wrong for monitoring
    purposes.

    Instead, each class that provides an offset **must** inherit this mixin, and
    subtract ``self.offset`` in `doRead()`, while adding it in `doStart()`.

    The device position is ``hardware_position - offset``.
    """
    parameters = {
        'offset':  Param('Offset of device zero to hardware zero', unit='main',
                         settable=True, category='offsets', chatty=True),
    }

    def doWriteOffset(self, value):
        """Adapt the limits to the new offset."""
        old_offset = self.offset
        diff = value - old_offset
        if isinstance(self, HasLimits):
            self._adjustLimitsToOffset(value, diff)
        # Since offset changes directly change the device value, refresh
        # the cache instantly here
        if self._cache:
            self._cache.put(self, 'value', self.read(0) - diff,
                            currenttime(), self.maxage)
        session.elog_event('offset', (str(self), old_offset, value))


class HasPrecision(DeviceMixinBase):
    """
    Mixin class for Readable and Moveable devices that want to provide a
    'precision' parameter.

    This is mainly useful for user info, and for high-level devices that have to
    work with limited-precision subordinate devices.
    """
    parameters = {
        'precision': Param('Precision of the device value', unit='main',
                           settable=True, category='precisions'),
    }


class HasMapping(DeviceMixinBase):
    """
    Mixin class for devices that use a finite mapping between user supplied
    input and internal representation.

    This is mainly useful for devices which can only yield certain values or go
    to positions from a predefined set, like switching devices.

    Abstract classes that use this mixin are implemented in
    `nicos.devices.abstract.MappedReadable` and `.MappedMoveable`.
    """
    parameters = {
        'mapping':  Param('Mapping of device values to raw (internal) values',
                          unit='', settable=False, mandatory=True,
                          type=dictof(str, anytype)),
        'fallback': Param('Readback value if the raw device value is not in the '
                          'mapping or None to disable', default=None,
                          unit='', type=anytype, settable=False),
    }

    # mapped values usually are string constants and have no unit
    parameter_overrides = {
        'unit':      Override(mandatory=False),
    }

    def doIsAllowed(self, target):
        if target not in self.mapping:
            return False, 'unknown value: %r, must be one of %s' % \
                (target, ', '.join(map(repr, sorted(self.mapping))))
        return True, ''


class Measurable(Readable):
    """
    Base class for devices used for data acquisition.

    Subclasses *need* to implement:

    * doRead()
    * doSetPreset(**preset)
    * doStart()
    * doStop()
    * doIsCompleted()

    Subclasses *can* implement:

    * doPause()
    * doResume()
    * doTime()
    * doSimulate()
    * doSave()
    * valueInfo()
    * presetInfo()
    """

    parameter_overrides = {
        'unit':  Override(description='(not used)', mandatory=False),
    }

    def _setMode(self, mode):
        # overwritten from Readable: don't read out detectors, it's not useful
        self._sim_active = mode == SIMULATION and self.hardware_access
        Device._setMode(self, mode)

    @usermethod
    def setPreset(self, **preset):
        """Set the new standard preset for this detector.

        .. method:: doSetPreset(**preset)

           This method must be present and is called to apply presets to the
           detector.  Preset names can be any string, corresponding to some kind
           of preselection that the detector supports.

           Usually a 't' preset (time in seconds) is supported.

           The dictionary passed contains the keys for *all* detectors that
           participate in a measurement, so you should only process those that
           the class understands and leave others alone.

           The `presetInfo` method is called to determine the presets that the
           class supports.
        """
        self.doSetPreset(**preset)

    @usermethod
    def start(self, **preset):
        """Start measurement, with either the given preset or the standard
        preset.  If a preset is given, `doSetPreset` is called with that preset
        first.

        This operation is forbidden in slave mode.

        .. method:: doStart()

           This method must be present and is called to start the measurement.
        """
        if self._mode == SLAVE:
            raise ModeError(self, 'start not possible in slave mode')
        elif self._sim_active:
            if hasattr(self, 'doTime'):
                time = self.doTime(preset)
            else:
                if 't' in preset:
                    time = preset['t']
                else:
                    time = 0
            session.clock.tick(time)
            self._sim_preset = preset
            return
        if preset:
            self.doSetPreset(**preset)
        self.doStart()

    def __call__(self, pos=None):  # pylint: disable=W0221
        """Allow dev(), but not dev(pos)."""
        if pos is None:
            return self.read()
        raise UsageError(self, 'device cannot be moved')

    def duringMeasureHook(self, elapsed):
        """Hook called during measurement.

        This can be overridden in subclasses to perform some periodic action
        while measuring.  The hook is called by `.count` for every detector in
        a loop.  The *elapsed* argument is the time elapsed since the detector
        was started.
        """

    @usermethod
    def pause(self):
        """Pause the measurement, if possible.

        Return True if paused successfully.  This operation is forbidden in
        slave mode.

        .. method:: doPause()

           If present, this is called to pause the measurement.  Otherwise,
           ``False`` is returned to indicate that pausing is not possible.
        """
        if self._mode == SLAVE:
            raise ModeError(self, 'pause not possible in slave mode')
        elif self._sim_active:
            return True
        if hasattr(self, 'doPause'):
            return self.doPause()
        return False

    @usermethod
    def resume(self):
        """Resume paused measurement.

        Return True if resumed successfully.  This operation is forbidden in
        slave mode.

        .. method:: doResume()

           If present, this is called to resume the measurement.  Otherwise,
           ``False`` is returned to indicate that resuming is not possible.
        """
        if self._mode == SLAVE:
            raise ModeError(self, 'resume not possible in slave mode')
        elif self._sim_active:
            return True
        if hasattr(self, 'doResume'):
            return self.doResume()
        return False

    @usermethod
    def stop(self):
        """Stop measurement now.

        This operation is forbidden in slave mode.

        .. method:: doStop()

           This method must be present and is called to actually stop the
           measurement.

        The `stop` method will return the device status after stopping.
        """
        if self._mode == SLAVE:
            raise ModeError(self, 'stop not possible in slave mode')
        elif self._sim_active:
            return
        self.doStop()

    @usermethod
    def isCompleted(self):
        """Return true if measurement is complete.

        .. method:: doIsCompleted()

           This method must be present and is called to determine if the
           measurement is completed.
        """
        if self._sim_active:
            return True
        return self.doIsCompleted()

    @usermethod
    def wait(self):
        """Wait for completion of the measurement.

        This is implemented by calling :meth:`isCompleted` in a loop.
        """
        while not self.isCompleted():
            sleep(0.1)

    @usermethod
    def read(self, maxage=None):
        """Return a tuple with the result(s) of the last measurement."""
        if self._sim_active:
            if hasattr(self, 'doSimulate'):
                result = self.doSimulate(self._sim_preset)
                if not isinstance(result, list):
                    return [result]
                return result
            return [0] * len(self.valueInfo())
        # always get fresh result from cache => maxage parameter is ignored
        if self._cache:
            self._cache.invalidate(self, 'value')
        result = self._get_from_cache('value', self.doRead)
        if not isinstance(result, list):
            return [result]
        return result

    def doPrepare(self):
        pass

    @usermethod
    def prepare(self):
        """Prepare measurement before counting.

        .. method: doPrepare

           If present, this is called to prepare the measurement.  This method
           will be called before start counting and e.g. for scans before
           moving to the next scan point.

        """
        if not self._sim_active:
            return self.doPrepare()

    def save(self, exception=False):
        """Save the current measurement, if necessary.

        Called by `.count` for all detectors at the end of a counting.  If
        *exception* is true, the counting was stopped due to an exception.

        .. method:: doSave(exception=False)

           This method can be implemented if the detector needs to save data.
        """
        if self._sim_active:
            return
        if hasattr(self, 'doSave'):
            self.doSave(exception)

    def info(self):
        """Automatically add device status (if not OK).  Does not add the
        device value since that is typically not useful for Measurables.
        """
        try:
            st = self.status()
        except Exception as err:
            self.log.warning('error getting status for info()', exc=err)
            yield ('status', 'status', 'Error: %s' % err)
        else:
            if st[0] not in (status.OK, status.UNKNOWN):
                yield ('status', 'status', '%s: %s' % st)
        for item in Device.info(self):
            yield item

    def valueInfo(self):
        """Describe the values measured by this device.

        Return a tuple of :class:`~nicos.core.params.Value` instances describing
        the values that :meth:`read` returns.

        This must be overridden by every Measurable that returns more than one
        value in a list.  The default indicates a single return value with no
        additional info about the value type.
        """
        return Value(self.name, unit=self.unit),

    def presetInfo(self):
        """Return an iterable of preset keys accepted by this device.

        The default implementation returns only a 't' (time) preset.  This must
        be overridden by all measurables that support more presets.
        """
        return ('t',)


# Use the DeviceMixinMeta metaclass here to provide the instancecheck
# Not derived from DeviceMixinBase as this class is not a mixin.
@add_metaclass(DeviceMixinMeta)
class NoDevice(object):
    """A class that represents "no device" attached to a :class:`DeviceAlias`."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<none>'

    def __getattr__(self, name):
        raise ConfigurationError('alias %r does not point to any device' % self.name)

    def __setattr__(self, name, value):
        if name != 'name':
            raise ConfigurationError('alias %r does not point to any device' % self.name)
        object.__setattr__(self, name, value)


class DeviceAlias(Device):
    """
    Generic "alias" device that can point all access to any other NICOS device.

    The device that should be accessed is set using the "alias" parameter, which
    can be configured and changed at runtime.  For example, with a DeviceAlias
    instance *T*::

        T.alias = Tcryo
        read(T)   # will read Tcryo
        T.alias = Toven
        read(T)   # will read Toven

    This allows to call e.g. the sample temperature by the same name in all
    sample environment setups, but behind the scenes implement it using
    different actual hardware devices.

    If the "alias" parameter is empty, the alias points to a special "NoDevice"
    object that raises a `ConfigurationError` on every access.
    """

    parameters = {
        'alias':    Param('Device to alias', type=none_or(nicosdev),
                          settable=True, chatty=True),
        'devclass': Param('Class name that the aliased device must be an '
                          'instance of', type=str, default='nicos.core.device.Device'),
    }

    _ownattrs = ['_obj', '_mode', '_cache', 'alias']
    _ownparams = set(['alias', 'name', 'devclass'])
    _initialized = False

    __display__ = True

    def __init__(self, name, **config):
        self._obj = None
        devclass = config.get('devclass', 'nicos.core.device.Device')
        try:
            modname, clsname = devclass.rsplit('.', 1)
            self._cls = session._nicos_import(modname, clsname)
        except Exception:
            self.log.warning('could not import class %r; using Device as the '
                             'alias devclass', exc=1)
            self._cls = Device
        Device.__init__(self, name, **config)
        if self._cache and self._mode in (MASTER, MAINTENANCE):
            # re-set alias to configured device every time... necessary to clean
            # up old assignments pointing to now nonexisting devices
            self.alias = config.get('alias', self._cache.get(self, 'alias', ''))
        self._initialized = True

    def __repr__(self):
        if isinstance(self._obj, NoDevice):
            return '<device %s, device alias pointing to nothing>' % self._name
        if not self.description:
            return '<device %s, alias to %s>' % (self._name, self._obj)
        return '<device %s, alias to %s "%s">' % (self._name, self._obj,
                                                  self.description)

    def doUpdateAlias(self, devname):
        if not devname:
            self._obj = NoDevice(str(self))
            if self._cache:
                self._cache.unsetRewrite(str(self))
                self._reinitParams()
        else:
            try:
                newdev = session.getDevice(devname, (self._cls, DeviceAlias),
                                           source=self)
            except NicosError:
                if not self._initialized:
                    # should not raise an error, otherwise the device cannot
                    # be created at all
                    fromconfig = self._config.get('alias', 'nothing')
                    self.log.warning('could not find aliased device %s, pointing '
                                     'to target from setup file (%s)' %
                                     (devname, fromconfig))
                    if 'alias' not in self._config:
                        newdev = None
                    else:
                        try:
                            newdev = session.getDevice(self._config['alias'],
                                                       (self._cls, DeviceAlias),
                                                       source=self)
                        except NicosError:
                            self.log.error('could not find target from setup '
                                           'file either, pointing to nothing',
                                           exc=1)
                            newdev = None
                else:
                    raise
            if newdev is self:
                raise NicosError(self, 'cannot set alias pointing to itself')
            if newdev != self._obj:
                self._obj = newdev
                if self._cache:
                    self._cache.setRewrite(str(self), devname)
                    self._reinitParams()

    def _reinitParams(self):
        if self._mode != MASTER:  # only in the copy that changed the alias
            return
        # clear all cached parameters
        self._cache.clear(str(self), exclude=self._ownparams)
        # put the parameters from the original device in the cache under the
        # name of the alias
        if not isinstance(self._obj, Device):
            return
        for pname in self._obj.parameters:
            if pname in self._ownparams:
                continue
            self._cache.put(self, pname, getattr(self._obj, pname))

    # Device methods that would not be alias-aware

    def valueInfo(self):
        # override to replace name of the aliased device with the alias' name
        new_info = []
        rx = r'^%s\b' % re.escape(self._obj.name)
        for v in self._obj.valueInfo():
            new_v = v.copy()
            # replace dev name, if at start of value name, with alias name
            new_v.name = re.sub(rx, self.name, v.name)
            new_info.append(new_v)
        return tuple(new_info)

    @usermethod
    def info(self):
        # override to use the object's "info" but add a note about the alias
        if isinstance(self._obj, Device):
            for v in self._obj.info():
                yield v
        yield ('instrument', 'alias', str(self._obj))

    @usermethod
    def version(self):
        v = []
        if isinstance(self._obj, Device):
            v = self._obj.version()
        v.extend(Device.version(self))
        return v

    # these methods must not be proxied

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    def shutdown(self):
        # re-implemented from Device to avoid running doShutdown
        # of the pointed-to device prematurely
        self.log.debug('shutting down device')
        if self._mode != SIMULATION:
            # remove subscriptions to parameter value updates
            if self._cache:
                for param, func in self._subscriptions:
                    self._cache.removeCallback(self, param, func)
        session.devices.pop(self._name, None)
        session.explicit_devices.discard(self._name)

    # generic proxying of missing attributes to the object

    def __getattr__(self, name):
        if not self._initialized:
            raise AttributeError(name)
        else:
            if name in DeviceAlias._ownattrs:
                return object.__getattr__(self, name)
            return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in DeviceAlias._ownattrs or not self._initialized:
            object.__setattr__(self, name, value)
        else:
            setattr(self._obj, name, value)

    def __delattr__(self, name):
        if name in DeviceAlias._ownattrs or not self._initialized:
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
        setattr(DeviceAlias, name, make_method(name))
