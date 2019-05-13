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
#   Nikhil Biyani <nikhil.biyani@psi.ch>
#
# *****************************************************************************

from __future__ import absolute_import, division, print_function

import json
from time import time as currenttime

from nicos import session
from nicos.core import MASTER, POLLER, Override, Param, Readable, status, \
    tupleof
from nicos.pycompat import iteritems

from nicos_ess.devices.kafka.consumer import KafkaSubscriber


class KafkaStatusHandler(KafkaSubscriber, Readable):
    """ Communicates with Kafka and receives status updates.
    The communicator also allows to communicate the status messages
    via callback providing new status messages and their timestamps.
    """

    parameters = {
        'statustopic': Param('Kafka topic where status messages are written',
                             type=str, settable=False, preinit=True,
                             mandatory=True, userparam=False),
        'statusinterval': Param('Expected time (secs) interval for the status '
                                'message updates',
                                type=int, default=20, settable=True,
                                userparam=False),
        'curstatus': Param('Store the current device status',
                           internal=True, type=tupleof(int, str),
                           settable=True, ),
        'nextupdate': Param('Time when the next message is expected', type=int,
                            internal=True, settable=True)
    }

    parameter_overrides = {
        'unit': Override(mandatory=False, userparam=False),
    }

    def doPreinit(self, mode):
        KafkaSubscriber.doPreinit(self, mode)
        if session.sessiontype != POLLER:
            self.subscribe(self.statustopic)

        # Initialize the next update time
        self._setROParam('nextupdate', currenttime() + self.statusinterval)

        # Rewrite the status on each startup
        if self._mode == MASTER:
            self._setROParam('curstatus', (status.OK, 'Updating status..'))

    def doRead(self, maxage=0):
        return ''

    def doStatus(self, maxage=0):
        return self.curstatus

    def new_messages_callback(self, messages):
        json_messages = {}
        for timestamp, msg in iteritems(messages):
            try:
                js = json.loads(msg)
                json_messages[timestamp] = js
                field = 'next_message_eta_ms'
                interval = (js[field] / 1000 if field in js else
                            self.statusinterval)
                next_update = timestamp / 1000 + interval
                if next_update > self.nextupdate:
                    self._setROParam('nextupdate', next_update)
            except Exception:
                self.log.warning('Could not decode message from status topic.')

        if json_messages:
            self._status_update_callback(json_messages)

        # Check if the process is still running
        if self._mode == MASTER and not self.is_process_running():
            self._setROParam('curstatus', (status.ERROR, 'Process down!'))

    def is_process_running(self):
        # Wait for some time to ensure that the message is written
        message_flush_buffer = 10
        now = currenttime()
        if self.nextupdate + message_flush_buffer < now:
            return False

        return True

    def _status_update_callback(self, messages):
        """This method is called whenever a new status messages appear on
        the status topic. The subclasses should define this method if
        a callback is required when new status messages appear.
        :param messages: dict of timestamp and message in JSON format
        """
        pass
