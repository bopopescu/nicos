description = 'setup for the status monitor'
group = 'special'

_collimationcolumn = Column(
    Block('Collimation',[
        BlockRow(
            Field(dev='att', name='att',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['x10','x100','x1000','OPEN'],
                  width=6.5,height=9),
            Field(dev='ng_pol', name='ng_pol',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','POL2','POL1','NG'],
                  width=5.5,height=9),
            Field(dev='col_20a', name='20a',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_20b', name='20b',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='bg1', name='bg1',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['50mm','OPEN','20mm','42mm'],
                  disabled_options = ['N.A.'],
                  width=7,height=9),
            Field(dev='col_16a', name='16a',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_16b', name='16b',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_12a', name='12a',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_12b', name='12b',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_8a', name='8a',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_8b', name='8b',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='bg2', name='bg2',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['28mm','20mm','12mm','OPEN'],
                  disabled_options = ['N.A.'],
                  width=7,height=9),
            Field(dev='col_4a', name='4a',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_4b', name='4b',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_2a', name='2a',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='col_2b', name='2b',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['LAS','free','COL','NG'],
                  width=5,height=9),
            Field(dev='sa1', name='sa1',
                  widget='nicos_mlz.sans1.gui.monitorwidgets.CollimatorTable',
                  options=['20mm','30mm','50x50'],
                  disabled_options = ['N.A.'],
                  width=7,height=9),
        ),
        BlockRow(
            Field(dev='bg1_m', name='bg1_m', format='%.1f', width=12),
            Field(dev='bg2_m', name='bg2_m', format='%.1f', width=12),
            Field(dev='sa1_m', name='sa1_m', format='%.1f', width=12),
        ),
        BlockRow(
            Field(dev='att_m', name='att_m', format='%.1f', width=12),
            Field(dev='col_20a_m', name='20a_m', format='%.1f', width=12),
            Field(dev='col_16a_m', name='16a_m', format='%.1f', width=12),
            Field(dev='col_12a_m', name='12a_m', format='%.1f', width=12),
            Field(dev='col_8a_m', name='8a_m', format='%.1f', width=12),
            Field(dev='col_4a_m', name='4a_m', format='%.1f', width=12),
            Field(dev='col_2a_m', name='2a_m', format='%.1f', width=12),
        ),
        BlockRow(
            Field(dev='ng_pol_m', name='ng_pol_m', format='%.1f', width=12),
            Field(dev='col_20b_m', name='20b_m', format='%.1f', width=12),
            Field(dev='col_16b_m', name='16b_m', format='%.1f', width=12),
            Field(dev='col_12b_m', name='12b_m', format='%.1f', width=12),
            Field(dev='col_8b_m', name='8b_m', format='%.1f', width=12),
            Field(dev='col_4b_m', name='4b_m', format='%.1f', width=12),
            Field(dev='col_2b_m', name='2b_m', format='%.1f', width=12),
        ),
        BlockRow(
            Field(dev='col', name='col'),
        ),
        ],
    ),
)



devices = dict(
    Monitor = device('nicos.services.monitor.qt.Monitor',
                     title = 'SANS-1 status monitor',
                     loglevel = 'debug',
#                     loglevel = 'info',
                     cache = 'sans1ctrl.sans1.frm2',
                     prefix = 'nicos/',
                     font = 'Luxi Sans',
                     valuefont = 'Consolas',
                     fontsize = 15,#12
                     padding = 0,#3
                     layout = [
                                 Row(_collimationcolumn),
                               ],
                    ),
)
