#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS-NG, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
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

"""The NICOS electronic logbook."""

__version__ = "$Revision$"

from os import path
from cgi import escape
from time import strftime, localtime
from shutil import copyfile

from nicos.elog.utils import formatMessage, pretty1, pretty2

try:
    import creole
except ImportError:
    creole = None

FRAMESET = '''\
<html>
<head>
<title>%s logbook: %s</title>
</head>
<frameset cols="200,*">
<frame src="toc.html">
<frame src="content.html" name="content">
</frameset>
</html>
'''

PROLOG = '''\
<html>
<head>
<style type="text/css">
body      { font-family: 'Arial', 'Helvetica', sans-serif; }
.remark   { font-weight: bold; }
.sample   { font-weight: bold; }
.attach:before  { content: url('data:image/png;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAcAAAAPAQMAAAASz0f9AAAAFXRFWHRDcmVhdGlvbiBUaW1lAAfT\
AgsIESPfE/DqAAAAB3RJTUUH0wILCBE0icGWXQAAAAlwSFlzAAAK8AAACvABQqw0mAAAAAZQTFRF\
////AAAAVcLTfgAAAB5JREFUeNpjkGFQAkJlIF4NhKvAcDXDZoYmBheGGgBQzQaaI6OKqAAAAABJ\
RU5ErkJggg=='); margin-right: 10px; }
.time     { font-size: small; float: right; background-color: #eee; }
.msgblock { cursor: pointer; margin-left: 20px; }
.msglabel { font-size: small; border: 1px solid #ccc;
            background-color: #eee; }
.messages { display: none; margin: 0; border: 1px solid #ccc;
            background-color: #eee; }
.messages .debug { color: #666; }
.messages .input { font-weight: bold; }
.messages .warn  { color: #c000c0; }
.messages .err   { font-weight: bold; color: #c00000; }
body > ul.toc { padding-left: 0; }
ul.toc        { padding-left: 25px; }
table     { border-collapse: collapse; }
td, th    { border: 1px solid #ccc; padding: 3px; }
th        { text-align: left; }
.scan     { width: 100%; }
.scannum  { font-weight: bold; }
</style>
<script type="text/javascript">
function hideshow(divel) {
  var pre = divel.childNodes[1];
  var span = divel.childNodes[0];
  if (pre.style.display == 'block') {
    pre.style.display = 'none';
    span.style.display = 'inline';
  } else {
    pre.style.display = 'block';
    span.style.display = 'none';
  }
}
function msgshow() {
  var els = document.getElementsByClassName('msgblock');
  for (var i = 0; i < els.length; i++) {
    els[i].childNodes[0].style.display = 'none';
    els[i].childNodes[1].style.display = 'block';
  }
}
function msghide() {
  var els = document.getElementsByClassName('msgblock');
  for (var i = 0; i < els.length; i++) {
    els[i].childNodes[0].style.display = 'inline';
    els[i].childNodes[1].style.display = 'none';
  }
}
</script>
<title>NICOS electronic logbook</title>
</head>
<body>
'''

PROLOG_TOC = '''\
<p style="font-size: small">
  <a href="javascript:parent.content.msgshow()">Show all messages</a><br>
  <a href="javascript:parent.content.msghide()">Hide all messages</a>
</p>
<p><b>Contents</b></p>
'''


class HtmlWriter(object):
    def __init__(self):
        self.fd = None
        self.curstate = None
        self.statesuffix = None
        self.fd_toc = None
        self.toc_level = 0
        self.curid = 0
        self.idstart = strftime('%Y%m%d%H%M%S')

    def close(self):
        self.endstate()
        self.fd.close()
        self.fd_toc.write('</ul>' * self.toc_level)
        self.fd_toc.close()
        self.toc_level = 0

    def open(self, dir, instr, proposal):
        if self.fd:
            self.close()
        open(path.join(dir, 'logbook.html'), 'w').write(
            FRAMESET % (instr, proposal))
        self.fd = open(path.join(dir, 'content.html'), 'a+b')
        self.fd.seek(0, 2)
        if self.fd.tell() == 0:
            self.fd.write(PROLOG)
            self.fd.flush()
        self.fd_toc = open(path.join(dir, 'toc.html'), 'a+b')
        self.fd_toc.seek(0, 2)
        if self.fd_toc.tell() == 0:
            self.fd_toc.write(PROLOG + PROLOG_TOC)
            self.fd_toc.flush()

    def emit(self, html):
        if self.fd:
            self.fd.write(html)
            self.fd.flush()

    def newstate(self, state, prefix, suffix, html):
        if state != self.curstate:
            self.endstate()
            self.statesuffix = suffix
            self.curstate = state
            self.emit(prefix)
        self.emit(html)

    def timestamp(self, time):
        self.newstate('plain', '', '', '<span class="time">%s</span>' %
                      strftime('%Y-%m-%d %H:%M:%S', localtime(time)))

    def endstate(self):
        if self.curstate:
            self.emit(self.statesuffix)
            self.curstate = None

    def emit_toc(self, html):
        if self.fd_toc:
            self.fd_toc.write(html)
            self.fd_toc.flush()

    def toc_entry(self, level, text, target):
        html = ''
        if self.toc_level < level:
            html += '<ul class="toc">' * (level - self.toc_level)
        elif self.toc_level > level:
            html += '</ul>' * (self.toc_level - level)
        html += ('<li class="toc"><a href="content.html#%s" '
                 'target="content">%s</a></li>' % (target, escape(text)))
        self.emit_toc(html)
        self.toc_level = level

    def new_id(self):
        self.curid += 1
        return 'id%s-%s' % (id(self), self.curid)


class Handler(object):
    def __init__(self, log):
        self.log = log
        self.handlers = {}
        # register all handlers
        for name, func in Handler.__dict__.iteritems():
            if name.startswith('handle_'):
                self.handlers[name[7:].replace('_', '/')] = getattr(self, name)

        self.dir = self.logdir = None
        self.out = HtmlWriter()

    def close(self):
        self.out.close()

    def handle_directory(self, time, data):
        directory, instr, proposal = data
        self.dir = directory
        self.logdir = path.join(directory, 'logbook')
        self.out.open(self.logdir, instr or 'NICOS', proposal)
        self.log.info('Openend new output file in ' + directory)

    def handle_newexperiment(self, time, data):
        proposal, title = data
        targetid = self.out.new_id()
        text = 'Experiment %s: %s' % (escape(proposal), escape(title))
        self.out.timestamp(time)
        self.out.newstate('plain', '', '',
                          '<h1 id="%s">%s</h1>\n' % (targetid, text))
        self.out.toc_entry(1, text, targetid)

    def handle_setup(self, time, setupnames):
        self.out.timestamp(time)
        self.out.newstate('plain', '', '',
            '<p class="setup">New setup: %s</p>\n' % setupnames)

    def handle_entry(self, time, data):
        if creole:
            data, headers = creole.translate(data, self.out.new_id)
        else:
            data, headers = escape(data), []
        self.out.newstate('entry', '', '', data)
        for level, text, targetid in headers:
            self.out.toc_entry(level, text, targetid)

    def handle_remark(self, time, remark):
        targetid = self.out.new_id()
        self.out.timestamp(time)
        self.out.newstate('plain', '', '',
            '<p id="%s" class="remark">%s</p>\n' % (targetid, escape(remark)))
        self.out.toc_entry(2, escape(remark), targetid)

    def handle_sample(self, time, data):
        self.out.timestamp(time)
        text = 'New sample: %s' % escape(data)
        targetid = self.out.new_id()
        self.out.toc_entry(2, text, targetid)
        self.out.newstate('plain', '', '',
            '<p id="%s" class="sample">%s</p>\n' % (targetid, text))

    def handle_detectors(self, time, dlist):
        self.out.timestamp(time)
        text = 'New standard detectors: %s' % escape(str(dlist))
        targetid = self.out.new_id()
        self.out.toc_entry(2, text, targetid)
        self.out.newstate('plain', '', '',
            '<p id="%s" class="detectors">%s</p>\n' % (targetid, text))

    def handle_environment(self, time, dlist):
        self.out.timestamp(time)
        text = 'New standard environment: %s' % escape(str(dlist))
        targetid = self.out.new_id()
        self.out.toc_entry(2, text, targetid)
        self.out.newstate('plain', '', '',
            '<p id="%s" class="environment">%s</p>\n' % (targetid, text))

    def handle_offset(self, time, data):
        self.out.timestamp(time)
        dev, old, new = data
        self.out.newstate('plain', '', '',
            '<p class="offset"><b>Adjustment:</b>' +
            escape('Offset of %s changed from %s to %s' % (dev, old, new))
            + '</p>\n')

    def handle_attachment(self, time, data):
        description, fpaths, names = data
        links = []
        for fpath, name in zip(fpaths, names):
            if not name:
                name = path.basename(fpath)
            fullname = path.join(self.logdir, name)
            oname = name; i = 0
            while path.exists(fullname):
                i += 1
                name = oname + str(i)
                fullname = path.join(self.logdir, name)
            copyfile(fpath, fullname)
            links.append('<a href="%s">%s</a>' % (name, escape(oname)))
        text = '<b>%s:</b> %s' % (escape(description) or 'Attachment',
                                  ' '.join(links))
        self.out.timestamp(time)
        self.out.newstate('plain', '', '', '<p class="attach">%s</p>\n' % text)

    def handle_message(self, time, message):
        msg = formatMessage(message)
        if msg:
            self.out.newstate('messages',
                '<div class="msgblock" onclick="hideshow(this)">'
                '<span class="msglabel">Messages</span>'
                '<pre class="messages">\n', '</pre></div>\n', msg)

    #def handle_scanbegin(self, time, dataset):
    #    print 'Scan begin:', dataset

    def handle_scanend(self, time, dataset):
        names = '+'.join(dataset.xnames)
        headers = ['Scan#'] + dataset.xnames + ['Plot', 'Data']
        scannumber = dataset.sinkinfo.get('number', -1)
        scanfile = dataset.sinkinfo.get('filename', '')
        if scannumber >= 0:
            html = ['<tr id="scan%s">' % scannumber]
            html.append('<td class="scannum">%s</td>' % scannumber)
        else:
            html = ['<tr>', '<td>-</td>']
        for i, xname in enumerate(dataset.xnames):
            first = dataset.xresults[0][i]
            last = dataset.xresults[-1][i]
            if first == last:
                html.append('<td>%s</td>' % pretty1(first))
            else:
                html.append('<td>%s</td>' % pretty2(first, last))
        # plot link
        #html.append('<td><a href="">Plot</a></td>')
        html.append('<td>...</td>')
        # file link
        if scanfile:
            relfile = path.relpath(path.join(
                self.dir, dataset.sinkinfo.get('filename')), self.logdir)
            html.append('<td><a href="%s" type="text/plain">File</a></td>'
                        % relfile)
        else:
            html.append('<td>...</td>')
        html.append('</tr>')
        self.out.newstate('scan-' + names, '<table class="scan"><tr>' +
            ''.join('<th>%s</th>' % escape(h) for h in headers) + '</tr>',
            '</table>\n', ''.join(html))


# TODO more ideas:
# - internal links -> reference scan numbers or attachments
# - integrated latex $foo$ syntax
# - count()s
# - show errors in messages (or at least summary: "1 error")
