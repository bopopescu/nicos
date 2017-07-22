# -*- coding: utf-8 -*-

description = 'Collimation setup'
group = 'lowlevel'
display_order = 10

excludes = ['virtual_collimation']

presets = configdata('config_collimation.COLLIMATION_PRESETS')

tango_base = 'tango://phys.kws1.frm2:10000/kws1/'

devices = dict(
    collimation = device('nicos_mlz.kws1.devices.collimation.Collimation',
                         description = 'high-level collimation device',
                         mapping = dict((k, (v['guides'], v['ap_x'], v['ap_y']))
                                        for (k, v) in presets.items()),
                         guides = 'coll_guides',
                         slitpos = [2, 4, 8, 14, 20],
                         slits = ['aperture_02',
                                  'aperture_04',
                                  'aperture_08',
                                  'aperture_14',
                                  'aperture_20'],
                        ),

    coll_set    = device('nicos.devices.tango.DigitalOutput',
                         tangodevice = tango_base + 'fzjdp_digital/coll_write',
                         fmtstr = '%#x',
                         lowlevel = True,
                        ),
    coll_in     = device('nicos.devices.tango.DigitalInput',
                         tangodevice = tango_base + 'fzjdp_digital/coll_in',
                         fmtstr = '%#x',
                         lowlevel = True,
                        ),
    coll_out    = device('nicos.devices.tango.DigitalInput',
                         tangodevice = tango_base + 'fzjdp_digital/coll_out',
                         fmtstr = '%#x',
                         lowlevel = True,
                        ),
    coll_sync   = device('nicos.devices.tango.DigitalOutput',
                         tangodevice = tango_base + 'fzjdp_digital/sync_bit',
                         fmtstr = '%#x',
                         lowlevel = True,
                        ),
    coll_guides = device('nicos_mlz.kws1.devices.collimation.CollimationGuides',
                         description = 'positioning of the neutron guide elements',
                         output = 'coll_set',
                         input_in = 'coll_in',
                         input_out = 'coll_out',
                         sync_bit = 'coll_sync',
                         fmtstr = '%d',
                         timeout = 150.0,
                        ),

    aperture_20   = device('nicos_mlz.kws1.devices.collimation.CollimationSlit',
                           description = '20m aperture',
                           horizontal = 'aperture_20_x',
                           vertical = 'aperture_20_y',
                           openpos = (50.0, 50.0),
                           fmtstr = '%.1f x %.1f',
                           lowlevel = True,
                          ),
    aperture_14   = device('nicos_mlz.kws1.devices.collimation.CollimationSlit',
                           description = '14m aperture',
                           horizontal = 'aperture_14_x',
                           vertical = 'aperture_14_y',
                           openpos = (50.0, 50.0),
                           fmtstr = '%.1f x %.1f',
                           lowlevel = True,
                          ),
    aperture_08   = device('nicos_mlz.kws1.devices.collimation.CollimationSlit',
                           description = '8m aperture',
                           horizontal = 'aperture_08_x',
                           vertical = 'aperture_08_y',
                           openpos = (50.0, 50.0),
                           fmtstr = '%.1f x %.1f',
                           lowlevel = True,
                          ),
    aperture_04   = device('nicos_mlz.kws1.devices.collimation.CollimationSlit',
                           description = '4m aperture',
                           horizontal = 'aperture_04_x',
                           vertical = 'aperture_04_y',
                           openpos = (49.9, 49.9),
                           fmtstr = '%.1f x %.1f',
                           lowlevel = True,
                          ),
    aperture_02   = device('nicos_mlz.kws1.devices.collimation.CollimationSlit',
                           description = '2m aperture',
                           horizontal = 'aperture_02_x',
                           vertical = 'aperture_02_y',
                           openpos = (40.0, 40.0),
                           fmtstr = '%.1f x %.1f',
                           lowlevel = True,
                          ),

    aperture_20_x = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '20m aperture horizontal opening',
                           tangodevice = tango_base + 'fzjs7/aperture_20_x',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                          ),
    aperture_20_y = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '20m aperture vertical opening',
                           tangodevice = tango_base + 'fzjs7/aperture_20_y',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                          ),

    aperture_14_x = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '14m aperture horizontal opening',
                           tangodevice = tango_base + 'fzjs7/aperture_14_x',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                           abslimits = (1, 50.0),
                          ),
    aperture_14_y = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '14m aperture vertical opening',
                           tangodevice = tango_base + 'fzjs7/aperture_14_y',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                          ),

    ap_14_x_readout = device('nicos.devices.tango.AnalogInput',
                           tangodevice = tango_base + 'fzjdp_analog/ap_14_readout',
                           unit = 'steps',
                           lowlevel = True,
                          ),

    aperture_08_x = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '8m aperture horizontal opening',
                           tangodevice = tango_base + 'fzjs7/aperture_8_x',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                          ),
    aperture_08_y = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '8m aperture vertical opening',
                           tangodevice = tango_base + 'fzjs7/aperture_8_y',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                          ),

    aperture_04_x = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '4m aperture horizontal opening',
                           tangodevice = tango_base + 'fzjs7/aperture_4_x',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                           abslimits = (1, 49.9),
                          ),
    aperture_04_y = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '4m aperture vertical opening',
                           tangodevice = tango_base + 'fzjs7/aperture_4_y',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                           abslimits = (1, 49.9),
                          ),

    aperture_02_x = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '2m aperture horizontal opening',
                           tangodevice = tango_base + 'fzjs7/aperture_2_x',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                          ),
    aperture_02_y = device('nicos_mlz.kws1.devices.collimation.SlitMotor',
                           description = '2m aperture vertical opening',
                           tangodevice = tango_base + 'fzjs7/aperture_2_y',
                           unit = 'mm',
                           precision = 0.1,
                           lowlevel = True,
                          ),
)
