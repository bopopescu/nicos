#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2016 by the NICOS contributors (see AUTHORS)
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

main_window = docked(
    vsplit(
        panel('status.ScriptStatusPanel', stopcounting=True),
#       panel('watch.WatchPanel'),
        panel('console.ConsolePanel'),
    ),
    ('NICOS devices',
     panel('devices.DevicesPanel', icons=True, dockpos='right',),
    ),
    ('Safety system',
     panel('toftof.gui.safetypanel.SafetyPanel'),
    ),
    ('Detector information',
     panel('generic.GenericPanel', uifile='custom/toftof/lib/gui/ratespanel.ui'),
    ),
    ('Experiment Information and Setup',
     panel('expinfo.ExpInfoPanel')
    ),
)

windows = [
    window('Editor', 'editor',
        vsplit(
#           panel('scriptbuilder.CommandsPanel'),
            panel('editor.EditorPanel',
                  tools = [
#                     tool('Scan Generator',
#                          'tools.ScanTool'),
                  ],
                 ),
        ),
    ),
#   window('Setup', 'setup',
#       tabbed(('Experiment', panel('setup_panel.ExpPanel')),
#              ('Setups',     panel('setup_panel.SetupsPanel')),
#              ('Detectors/Environment', panel('setup_panel.DetEnvPanel')),
#       )
#   ),
#   window('Scans', 'plotter', panel('scans.ScansPanel'),),
    window('History', 'find', panel('history.HistoryPanel'),),
    window('Logbook', 'table', panel('elog.ELogPanel'),),
    window('Errors', 'errors', panel('errors.ErrorPanel'),),
    window('Live data', 'live', panel('live.LiveDataPanel',
                                      instrument = 'toftof'),),
]

tools = [
    tool('Downtime report', 'downtime.DownTimeTool',
         receiver='f.carsughi@fz-juelich.de',
         mailserver='smtp.frm2.tum.de',
         sender='toftof@frm2.tum.de',
        ),
    tool('Calculator', 'calculator.CalculatorTool'),
    tool('Neutron cross-sections', 'website.WebsiteTool',
         url='http://www.ncnr.nist.gov/resources/n-lengths/'),
    tool('Neutron activation', 'website.WebsiteTool',
         url='https://webapps.frm2.tum.de/intranet/activation/'),
    tool('Neutron calculations', 'website.WebsiteTool',
         url='https://webapps.frm2.tum.de/intranet/neutroncalc/'),
    tool('Report NICOS bug or request enhancement', 'bugreport.BugreportTool'),
    tool('Emergency stop button', 'estop.EmergencyStopTool',
         runatstartup=False,),
]
