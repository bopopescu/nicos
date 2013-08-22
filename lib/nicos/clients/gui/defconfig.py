#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2013 by the NICOS contributors (see AUTHORS)
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

"""NICOS GUI default configuration."""

from nicos.clients.gui.config import vsplit, window, panel, tool, docked

config = ('Default', [
        docked(
            vsplit(
                panel('status.ScriptStatusPanel'),
#                panel('watch.WatchPanel'),
                panel('console.ConsolePanel'),
            ),
            ('NICOS devices',
             panel('nicos.clients.gui.panels.devices.DevicesPanel',
                   icons=True, dockpos='right',
                  )
            ),
            ('Experiment info', panel('nicos.clients.gui.panels.expinfo.ExpInfoPanel')),
        ),
        window('Setup', 'setup', True,
            panel('setup_panel.SetupPanel')),
        window('Editor', 'editor', True,
            vsplit(
                panel('scriptbuilder.CommandsPanel'),
                panel('editor.EditorPanel',
                  tools = [
                      tool('Scan', 'nicos.clients.gui.tools.scan.ScanTool')
                  ]))),
        window('Scans', 'plotter', True,
            panel('scans.ScansPanel')),
        window('History', 'find', True,
            panel('history.HistoryPanel')),
        window('Logbook', 'table', True,
            panel('elog.ELogPanel')),
        window('Log files', 'table', True,
            panel('logviewer.LogViewerPanel')),
        window('Errors', 'errors', True,
            panel('errors.ErrorPanel')),
        #window('Live data', 'live', True,
        #    panel('live.LiveDataPanel')),
        #window('TAS status', 'table', True,
        #    panel('generic.GenericPanel',
        #          uifile='custom/demo/gui/tasaxes.ui',
        #          dir='../../../..')),
    ], [
        tool('Calculator', 'calculator.CalculatorTool'),
        tool('Neutron cross-sections', 'website.WebsiteTool',
             url='http://www.ncnr.nist.gov/resources/n-lengths/'),
        tool('Neutron activation', 'website.WebsiteTool',
             url='http://www.wise-uranium.org/rnac.html'),
        tool('Report NICOS bug', 'website.WebsiteTool',
             url='http://trac.frm2.tum.de/redmine/projects/nicos/issues/new'),
        tool('Emergency stop button', 'estop.EmergencyStopTool',
             runatstartup=True),
    ]
)
