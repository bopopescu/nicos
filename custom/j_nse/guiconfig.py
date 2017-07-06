"""NICOS GUI default configuration."""

main_window = tabbed(
    ('Instrument', docked(
        vsplit(
            hsplit(
                vsplit(
                    panel('cmdbuilder.CommandPanel'),
                    panel('status.ScriptStatusPanel'),
                ),
            ),
            tabbed(
                ('All output',
                    panel('console.ConsolePanel',
                          hasinput=False, hasmenu=False)),
                ('Errors/Warnings',
                    panel('errors.ErrorPanel')),
            ),
        ),
        ('Experiment Info', panel('expinfo.ExpInfoPanel', dockpos='left')),
        ('NICOS devices',
            panel('devices.DevicesPanel', icons=True, dockpos='right')),
    )),
    ('Script Editor',
        vsplit(
            panel('scriptbuilder.CommandsPanel'),
            panel('editor.EditorPanel', tools = []),
        )),
    # ('Scan Plotting', panel('scans.ScansPanel')),
    ('Device Plotting', panel('history.HistoryPanel')),
    # ('Logbook', panel('elog.ELogPanel')),
)

windows = []

tools = [
    tool('Downtime report', 'downtime.DownTimeTool',
         receiver='f.carsughi@fz-juelich.de',
         mailserver='smtp.frm2.tum.de',
         sender='j-nse@frm2.tum.de',
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
         runatstartup=True),
]