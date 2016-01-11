"""SANS1 GUI default configuration."""

# evaluated by code in : nicos.clients.gui.panels.__init__.createWindowItem

# vsplit( content1, content2, ... )
# hsplit( content1, content2, ... )
# tapped( (tabname1, content1), (tabname2, content2),... )
# docked( content1, (tabname, content2), ... )
## if with tabname, content panels can be stacked, then a tabbar is displayed with the tabnames..

# window( <Button/WindowName>, <icon-name>, bool, content )
# icons are defined in resources/nicos-gui.qrc
## known icons: setup, editor, plotter, find, table, errors, live

# tool( Menu-entry-str, <modulepath>, [, kwargs ] )
## options for all: runatstartup=True/False
## known <modulepaths> below nicos.clients.gui.tools:
# 'calculator.CalculatorTool'
# 'website.WebsiteTool'
# 'estop.EmergencyStopTool'
# 'scan.ScanTool'
# 'commands.CommandsTool'

# panel( <modulepath> [, kwargs ] )
## known <modulepath> below nicos.clients.gui.panels:
# 'cmdbuilder.CommandPanel'
# 'commandline.CommandLinePanel'
# 'console.ConsolePanel'
# 'devices.DevicesPanel' icons = True/False: Show/hide status icons
# 'editor.EditorPanel'
# 'elog.ELogPanel'
# 'errors.ErrorPanel'
# 'expinfo.ExpInfoPanel'
# 'generic.GenericPanel'  loads an uifile='path-to-uifile.ui' from dir='directory-containing-ui-file', also connects to cache....
# 'history.HistoryPanel'
# 'live.LiveDataPanel'
# 'logviewer.LogViewerPanel'
# 'scans.ScansPanel'
# 'scriptbuilder.CommandsPanel'
# 'setup_panel.SetupPanel'
# 'status.ScriptStatusPanel'
# 'watch.WatchPanel'



# config = (ignored, [Mainwindow + N*window(...)], [tools])
config = ('Default', [
        docked(
            vsplit(
                panel('status.ScriptStatusPanel'),
#               panel('watch.WatchPanel'),
                panel('console.ConsolePanel'),
            ),
            # ('Watch Expressions',panel('watch.WatchPanel')),
            ('NICOS devices',
             panel('devices.DevicesPanel', icons=True, dockpos='right',)
            ),
            ('Experiment info', panel('expinfo.ExpInfoPanel')),
        ),
        window('Setup', 'setup',
            tabbed(
                ('Experiment',
                    panel('setup_panel.ExpPanel')),
                ('Setups',
                    panel('setup_panel.SetupsPanel')),
                ('Detectors/Environment',
                    panel('setup_panel.DetEnvPanel')),
                ('Samples',
                    panel('sans1.gui.samplechanger.SamplechangerSetupPanel',
                          # image='custom/sans1/lib/gui/sampleChanger11.png',
                          image='custom/sans1/lib/gui/sampleChanger22.png',
                          # positions = 11, setups='!setup22',)),
                          positions = 22, setups='sc1',
                         ),
                ),
            )
        ),
        window('Editor', 'editor',
            vsplit(
                panel('scriptbuilder.CommandsPanel'),
                panel('editor.EditorPanel',
                    tools = [
                            tool('Scan', 'scan.ScanTool')
                            ]
                    )
                )
        ),
        window('Watches', 'leds/blue_on',
            panel('watch.WatchPanel')),
        window('Scans', 'plotter',
            panel('scans.ScansPanel')),
        window('History', 'find',
            panel('history.HistoryPanel')),
        window('Logbook', 'table',
            panel('elog.ELogPanel')),
        window('Log files', 'table',
            panel('logviewer.LogViewerPanel')),
        window('Errors', 'errors',
            panel('errors.ErrorPanel')),
    ], [
        tool('Downtime report', 'downtime.DownTimeTool',
             receiver='f.carsughi@fz-juelich.de',
             mailserver='smtp.frm2.tum.de',
             sender='sans1@frm2.tum.de',
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
             runatstartup=False),
        tool('Maintenance commands',
             'tools.commands.CommandsTool',
             commands=[
                 ('TACO server control panel (beta)',
                  'SSH_ASKPASS=/usr/bin/ssh-askpass setsid /usr/bin/ssh -XY '
                  'maint@sans1hw.sans1.frm2 "source /etc/tacoenv.sh && '
                  'sudo /usr/bin/python /opt/tacocp/tacocp.py '
                  'sans1srv.sans1.frm2" && exit',
                 ),
             ]),
    ]
)
