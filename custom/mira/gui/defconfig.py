# Default MIRA GUI config

from nicos.clients.gui.config import vsplit, hsplit, panel, window, tool

maint_commands = [
    ('Restart NICOS poller',
     'ssh maint@mira1 sudo /etc/init.d/nicos-system restart poller'),
    ('Restart NICOS daemon',
     'ssh maint@mira1 sudo /etc/init.d/nicos-system restart daemon'),
    ('Restart MIRA1 TACO servers',
     'ssh maint@mira1 sudo /usr/local/bin/taco-system restart'),
]


MIEZE_settings = [
    '46_69',
#    '65_97p5',
#    '74_111',
    '72_108',
#    '103_154p5',
    '99_148p5',
    '138_207',
    '139_208p5_BS',
    '200_300',
    '200_300_BS',
    '279_418p5_BS',
    '280_420',
]

config = ('Default', [
    vsplit(
        hsplit(
            panel('status.ScriptStatusPanel'),
            panel('watch.WatchPanel')),
        panel('console.ConsolePanel'),
        ),
    window('Setup', 'setup', True,
           panel('setup_panel.SetupPanel')),
    window('Editor', 'editor', True,
           panel('editor.EditorPanel',
                 tools = [
                     tool('Scan', 'nicos.clients.gui.tools.scan.ScanTool')
                 ])),
    window('Live data', 'live', True,
           panel('nicos.mira.gui.live.LiveDataPanel')),
    window('Scans', 'plotter', True,
           panel('scans.ScansPanel')),
    window('History', 'find', True,
           panel('history.HistoryPanel')),
    window('Devices', 'table', True,
           panel('devices.DevicesPanel')),
    window('Logbook', 'table', True,
           panel('elog.ELogPanel')),
    window('NICOS log files', 'table', True,
           panel('logviewer.LogViewerPanel')),
    ], [
        tool('Maintenance',
             'nicos.clients.gui.tools.commands.CommandsTool',
             commands=maint_commands),
        tool('Calculator',
             'nicos.clients.gui.tools.calculator.CalculatorTool',
             mieze=MIEZE_settings),
        tool('Neutron cross-sections',
             'nicos.clients.gui.tools.website.WebsiteTool',
             url='http://www.ncnr.nist.gov/resources/n-lengths/'),
        tool('Neutron activation',
             'nicos.clients.gui.tools.website.WebsiteTool',
             url='http://www.wise-uranium.org/rnac.html'),
        tool('MIRA Wiki',
             'nicos.clients.gui.tools.website.WebsiteTool',
             url='http://mira2.mira.frm2:8080/'),
        tool('Phone database',
             'nicos.clients.gui.tools.website.WebsiteTool',
             url='http://www.frm2.tum.de/intern/funktionen/phonedb/index.html'),
        tool('Report NICOS bug',
             'nicos.clients.gui.tools.website.WebsiteTool',
             url='http://trac.frm2.tum.de/redmine/projects/nicos/issues/new'),
    ]
)
