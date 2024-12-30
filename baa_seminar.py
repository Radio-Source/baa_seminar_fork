#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Baa Seminar
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import baa_seminar_baseline_compensate as baseline_compensate  # embedded python block
import baa_seminar_baseline_compensate_0 as baseline_compensate_0  # embedded python block
import baa_seminar_flipper as flipper  # embedded python block
import baa_seminar_flipper_0 as flipper_0  # embedded python block
import baa_seminar_formatter as formatter  # embedded python block
import baa_seminar_stripchart as stripchart  # embedded python block
import baa_seminar_stripchart_0 as stripchart_0  # embedded python block
import baa_seminar_stripchart_0_0 as stripchart_0_0  # embedded python block
import baa_seminar_stripchart_1 as stripchart_1  # embedded python block
import baa_seminar_stripchart_1_0 as stripchart_1_0  # embedded python block
import baa_seminar_stripchart_1_0_0 as stripchart_1_0_0  # embedded python block
import baa_seminar_vectorlogger as vectorlogger  # embedded python block
import baa_seminar_vectorlogger_0 as vectorlogger_0  # embedded python block
import math
import osmosdr
import time
import ra_funcs
import sip
import threading


def snipfcn_snippet_0(self):
    if (self.sync > 0):
    	self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)

class baa_seminar(gr.top_block, Qt.QWidget):

    def __init__(self, angleEast=0.0, angleWest=0.0, antenna="", baseline=4.0, bw=0.0, comp=0, dceast=0.0, dcwest=0.0, declination=45.0, device="rtl=0 rlt=1", dmult=1, freq=1420.4058e6, highpass=0, logtime=5.0, longitude=(-76.03), mulEast=1.0, mulWest=1.0, prefix="./", rfgain=40, seconds=3600, sinteg=10.0, srate=2.56e6, sync=0, tinteg=45, title="BAA Seminar", utc=1, velocity=1):
        gr.top_block.__init__(self, "Baa Seminar", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Baa Seminar")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "baa_seminar")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.angleEast = angleEast
        self.angleWest = angleWest
        self.antenna = antenna
        self.baseline = baseline
        self.bw = bw
        self.comp = comp
        self.dceast = dceast
        self.dcwest = dcwest
        self.declination = declination
        self.device = device
        self.dmult = dmult
        self.freq = freq
        self.highpass = highpass
        self.logtime = logtime
        self.longitude = longitude
        self.mulEast = mulEast
        self.mulWest = mulWest
        self.prefix = prefix
        self.rfgain = rfgain
        self.seconds = seconds
        self.sinteg = sinteg
        self.srate = srate
        self.sync = sync
        self.tinteg = tinteg
        self.title = title
        self.utc = utc
        self.velocity = velocity

        ##################################################
        # Variables
        ##################################################
        self.pacer = pacer = 0.0
        self.ifreq = ifreq = freq
        self.idecln = idecln = declination
        self.ibaseline = ibaseline = baseline
        self.gmt = gmt = time.gmtime()
        self.today = today = "%04d-%02d-%02d" % (gmt.tm_year, gmt.tm_mon, gmt.tm_mday)
        self.tiktok = tiktok = pacer*0.0
        self.samp_rate = samp_rate = int(srate)
        self.iangWest = iangWest = angleWest
        self.iangEast = iangEast = angleEast
        self.fper = fper = ra_funcs.fperiod(ifreq,ibaseline,idecln,0.0)
        self.fftsize = fftsize = 2048
        self.winpower = winpower = sum([x*x for x in window.blackman_harris(fftsize)])
        self.variable_qtgui_label_0_1_0 = variable_qtgui_label_0_1_0 = "%5d secs" % fper
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1 = title + " " + today
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0 = prefix
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = ra_funcs.cur_sidereal(longitude+tiktok).replace(",",":")
        self.tunereq = tunereq = uhd.tune_request(ifreq,(samp_rate/2.0)+100e3)
        self.split_ratio = split_ratio = 100
        self.phaseWest = phaseWest = complex(math.cos(math.radians(iangWest)),math.sin(math.radians(iangWest)))
        self.phaseEast = phaseEast = complex(math.cos(math.radians(iangEast)),math.sin(math.radians(iangEast)))
        self.itinteg = itinteg = tinteg
        self.isinteg = isinteg = sinteg
        self.is_usrp = is_usrp = "uhd" in device
        self.irfgain = irfgain = rfgain
        self.imulWest = imulWest = mulWest
        self.imulEast = imulEast = mulEast
        self.ihighpass = ihighpass = highpass
        self.idcwest = idcwest = dceast
        self.idceast = idceast = dceast
        self.freqstep = freqstep = (samp_rate/fftsize)/1.0e6
        self.freqlow = freqlow = (ifreq-(samp_rate/2.0))/1.0e6
        self.fftrate = fftrate = int(samp_rate/fftsize)
        self.doplow = doplow = -((samp_rate/2.0)/ifreq)*299792.0
        self.dophigh = dophigh = ((samp_rate/2.0)/ifreq)*299792.0
        self.dc_gain = dc_gain = dmult
        self.data_rate = data_rate = 10
        self.correct_baseline = correct_baseline = False
        self.actual_freq = actual_freq = ifreq

        ##################################################
        # Blocks
        ##################################################

        self.Main = Qt.QTabWidget()
        self.Main_widget_0 = Qt.QWidget()
        self.Main_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Main_widget_0)
        self.Main_grid_layout_0 = Qt.QGridLayout()
        self.Main_layout_0.addLayout(self.Main_grid_layout_0)
        self.Main.addTab(self.Main_widget_0, 'Total Power')
        self.Main_widget_1 = Qt.QWidget()
        self.Main_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Main_widget_1)
        self.Main_grid_layout_1 = Qt.QGridLayout()
        self.Main_layout_1.addLayout(self.Main_grid_layout_1)
        self.Main.addTab(self.Main_widget_1, 'Spectral')
        self.Main_widget_2 = Qt.QWidget()
        self.Main_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Main_widget_2)
        self.Main_grid_layout_2 = Qt.QGridLayout()
        self.Main_layout_2.addLayout(self.Main_grid_layout_2)
        self.Main.addTab(self.Main_widget_2, 'Correlation')
        self.Main_widget_3 = Qt.QWidget()
        self.Main_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Main_widget_3)
        self.Main_grid_layout_3 = Qt.QGridLayout()
        self.Main_layout_3.addLayout(self.Main_grid_layout_3)
        self.Main.addTab(self.Main_widget_3, 'Controls')
        self.top_grid_layout.addWidget(self.Main, 2, 0, 4, 4)
        for r in range(2, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._ifreq_tool_bar = Qt.QToolBar(self)
        self._ifreq_tool_bar.addWidget(Qt.QLabel("Tuned Frequency" + ": "))
        self._ifreq_line_edit = Qt.QLineEdit(str(self.ifreq))
        self._ifreq_tool_bar.addWidget(self._ifreq_line_edit)
        self._ifreq_line_edit.editingFinished.connect(
            lambda: self.set_ifreq(eng_notation.str_to_num(str(self._ifreq_line_edit.text()))))
        self.Main_grid_layout_3.addWidget(self._ifreq_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._idecln_tool_bar = Qt.QToolBar(self)
        self._idecln_tool_bar.addWidget(Qt.QLabel("Declination" + ": "))
        self._idecln_line_edit = Qt.QLineEdit(str(self.idecln))
        self._idecln_tool_bar.addWidget(self._idecln_line_edit)
        self._idecln_line_edit.editingFinished.connect(
            lambda: self.set_idecln(eng_notation.str_to_num(str(self._idecln_line_edit.text()))))
        self.Main_grid_layout_3.addWidget(self._idecln_tool_bar, 2, 1, 1, 1)
        for r in range(2, 3):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._itinteg_range = qtgui.Range(1, 500, 10, tinteg, 100)
        self._itinteg_win = qtgui.RangeWidget(self._itinteg_range, self.set_itinteg, "TP Integration Time", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._itinteg_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._isinteg_range = qtgui.Range(1, 3600, 30, sinteg, 100)
        self._isinteg_win = qtgui.RangeWidget(self._isinteg_range, self.set_isinteg, "Spectral Integration Time", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._isinteg_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(2, 3):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._irfgain_range = qtgui.Range(0, 100, 2.5, rfgain, 100)
        self._irfgain_win = qtgui.RangeWidget(self._irfgain_range, self.set_irfgain, "RF Gain", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._irfgain_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._imulWest_range = qtgui.Range(0.1, 1.5, 0.01, mulWest, 100)
        self._imulWest_win = qtgui.RangeWidget(self._imulWest_range, self.set_imulWest, "Gain Correction West", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._imulWest_win, 5, 1, 1, 1)
        for r in range(5, 6):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._imulEast_range = qtgui.Range(0.1, 1.5, 0.01, mulEast, 100)
        self._imulEast_win = qtgui.RangeWidget(self._imulEast_range, self.set_imulEast, "Gain Correction East", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._imulEast_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        _ihighpass_check_box = Qt.QCheckBox("Enable differential high pass")
        self._ihighpass_choices = {True: 1, False: 0}
        self._ihighpass_choices_inv = dict((v,k) for k,v in self._ihighpass_choices.items())
        self._ihighpass_callback = lambda i: Qt.QMetaObject.invokeMethod(_ihighpass_check_box, "setChecked", Qt.Q_ARG("bool", self._ihighpass_choices_inv[i]))
        self._ihighpass_callback(self.ihighpass)
        _ihighpass_check_box.stateChanged.connect(lambda i: self.set_ihighpass(self._ihighpass_choices[bool(i)]))
        self.Main_grid_layout_3.addWidget(_ihighpass_check_box, 0, 3, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(3, 4):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._idcwest_range = qtgui.Range(-0.01, 0.01, 0.0001, dceast, 400)
        self._idcwest_win = qtgui.RangeWidget(self._idcwest_range, self.set_idcwest, "DC Offset West", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._idcwest_win, 6, 2, 1, 2)
        for r in range(6, 7):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(2, 4):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._idceast_range = qtgui.Range(-0.01, 0.01, 0.0001, dceast, 400)
        self._idceast_win = qtgui.RangeWidget(self._idceast_range, self.set_idceast, "DC Offset East", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._idceast_win, 6, 0, 1, 2)
        for r in range(6, 7):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 2):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self.formatter = formatter.blk(formatter=None, filepat=prefix+'tp-%04d%02d%02d', extension='.csv', logtime=logtime, fmtstr='%11.9f', nchan=6, localtime=False if utc != 0 else True, longitude=longitude, legend="Sum,Corr(R),Corr(I),Diff,East,West,DEC=%f,FREQ=%f,BW=%f" % (idecln, ifreq/1.0e6, srate/1.0e6))
        self._dc_gain_range = qtgui.Range(1, 1000, 10, dmult, 100)
        self._dc_gain_win = qtgui.RangeWidget(self._dc_gain_range, self.set_dc_gain, "Detector Output Mult.", "counter", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._dc_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        _correct_baseline_check_box = Qt.QCheckBox("Baseline Correction")
        self._correct_baseline_choices = {True: True, False: False}
        self._correct_baseline_choices_inv = dict((v,k) for k,v in self._correct_baseline_choices.items())
        self._correct_baseline_callback = lambda i: Qt.QMetaObject.invokeMethod(_correct_baseline_check_box, "setChecked", Qt.Q_ARG("bool", self._correct_baseline_choices_inv[i]))
        self._correct_baseline_callback(self.correct_baseline)
        _correct_baseline_check_box.stateChanged.connect(lambda i: self.set_correct_baseline(self._correct_baseline_choices[bool(i)]))
        self.Main_grid_layout_1.addWidget(_correct_baseline_check_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.Main_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_1.setColumnStretch(c, 1)
        self.vectorlogger_0 = vectorlogger_0.blk(fftsize=fftsize, formatter=None, filepat=prefix+'fft-1-%04d%02d%02d', extension='.csv', logtime=logtime*3, fmtstr='%6.2f', localtime=False if utc != 0 else True, fftshift=False, longitude=longitude)
        self.vectorlogger = vectorlogger.blk(fftsize=fftsize, formatter=None, filepat=prefix+'fft-0-%04d%02d%02d', extension='.csv', logtime=logtime*3, fmtstr='%6.2f', localtime=False if utc != 0 else True, fftshift=False, longitude=longitude)
        self._variable_qtgui_label_0_1_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_1_0_formatter = None
        else:
            self._variable_qtgui_label_0_1_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_1_0_tool_bar.addWidget(Qt.QLabel("Fringe Period"))
        self._variable_qtgui_label_0_1_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_1_0_formatter(self.variable_qtgui_label_0_1_0)))
        self._variable_qtgui_label_0_1_0_tool_bar.addWidget(self._variable_qtgui_label_0_1_0_label)
        self.Main_grid_layout_3.addWidget(self._variable_qtgui_label_0_1_0_tool_bar, 2, 4, 1, 1)
        for r in range(2, 3):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(4, 5):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_1_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_1_formatter = None
        else:
            self._variable_qtgui_label_0_1_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_1_tool_bar.addWidget(Qt.QLabel("Name"))
        self._variable_qtgui_label_0_1_label = Qt.QLabel(str(self._variable_qtgui_label_0_1_formatter(self.variable_qtgui_label_0_1)))
        self._variable_qtgui_label_0_1_tool_bar.addWidget(self._variable_qtgui_label_0_1_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_1_tool_bar, 0, 3, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_0_formatter = None
        else:
            self._variable_qtgui_label_0_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_0_tool_bar.addWidget(Qt.QLabel("Logging to..."))
        self._variable_qtgui_label_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_0_formatter(self.variable_qtgui_label_0_0)))
        self._variable_qtgui_label_0_0_tool_bar.addWidget(self._variable_qtgui_label_0_0_label)
        self.Main_grid_layout_3.addWidget(self._variable_qtgui_label_0_0_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("LMST"))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.stripchart_1_0_0 = stripchart_1_0_0.blk(decim=data_rate, seconds=seconds)
        self.stripchart_1_0 = stripchart_1_0.blk(decim=data_rate, seconds=seconds)
        self.stripchart_1 = stripchart_1.blk(decim=data_rate, seconds=seconds)
        self.stripchart_0_0 = stripchart_0_0.blk(decim=data_rate, seconds=seconds)
        self.stripchart_0 = stripchart_0.blk(decim=data_rate, seconds=seconds)
        self.stripchart = stripchart.blk(decim=data_rate, seconds=seconds)
        self.single_pole_iir_filter_xx_1_0 = filter.single_pole_iir_filter_ff((ra_funcs.getalpha(1.0/isinteg,fftrate)), fftsize)
        self.single_pole_iir_filter_xx_1 = filter.single_pole_iir_filter_ff((ra_funcs.getalpha(1.0/isinteg,fftrate)), fftsize)
        self.single_pole_iir_filter_xx_0_1_0 = filter.single_pole_iir_filter_ff((ra_funcs.getalpha(1.0/(fper*1.25),samp_rate/split_ratio)), 1)
        self.single_pole_iir_filter_xx_0_1 = filter.single_pole_iir_filter_ff((ra_funcs.getalpha(1.0/itinteg,samp_rate/split_ratio)), 1)
        self.single_pole_iir_filter_xx_0_0_0 = filter.single_pole_iir_filter_cc((ra_funcs.getalpha(1.0/(fper*1.25),samp_rate/split_ratio)), 1)
        self.single_pole_iir_filter_xx_0_0 = filter.single_pole_iir_filter_cc((ra_funcs.getalpha(1.0/itinteg,samp_rate/split_ratio)), 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff((ra_funcs.getalpha(1.0/itinteg,samp_rate/split_ratio)), 1)
        self.qtgui_vector_sink_f_1 = qtgui.vector_sink_f(
            fftsize,
            doplow if velocity == True else freqlow,
            ((dophigh-doplow)/fftsize if velocity == True else freqstep),
            "Red shift(km/s)" if velocity == True else "Frequency (MHz)",
            'Rel power (dB)',
            "Doppler Velocity" if velocity == True else "Frequency",
            2, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_1.set_update_time((1.0/(data_rate)))
        self.qtgui_vector_sink_f_1.set_y_axis((-100), 10)
        self.qtgui_vector_sink_f_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_1.enable_grid(True)
        self.qtgui_vector_sink_f_1.set_x_axis_units("km/s" if velocity == True else "MHz")
        self.qtgui_vector_sink_f_1.set_y_axis_units('dB')
        self.qtgui_vector_sink_f_1.set_ref_level(0)


        labels = ["Spectrum East", "Spectrum West", '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_1.qwidget(), Qt.QWidget)
        self.Main_grid_layout_1.addWidget(self._qtgui_vector_sink_f_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.Main_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Main_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            seconds,
            0,
            1,
            "Time (Seconds)",
            "Cross Power",
            'Correlator Output',
            2, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.250)
        self.qtgui_vector_sink_f_0_0.set_y_axis((-1.0), 1.0)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units('Secs')
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)


        labels = ['COS', 'SIN', '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 2, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.Main_grid_layout_2.addWidget(self._qtgui_vector_sink_f_0_0_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.Main_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 4):
            self.Main_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            seconds,
            0,
            1,
            "Time (Seconds)",
            "Detector Power",
            "Total Power/Diff. Power",
            4, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.250)
        self.qtgui_vector_sink_f_0.set_y_axis(0, 1.5)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units('Secs')
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['Detector (Sum)', 'Detector (Difference)', 'Detector(East)', 'Detector(West)', '',
            '', '', '', '', '']
        widths = [2, 2, 2, 2, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "magenta", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(4):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.Main_grid_layout_0.addWidget(self._qtgui_vector_sink_f_0_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.Main_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.Main_grid_layout_0.setColumnStretch(c, 1)
        self.pacer_probe = blocks.probe_signal_f()
        def _pacer_probe():
          while True:

            val = self.pacer_probe.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_pacer,val))
              except AttributeError:
                self.set_pacer(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (1))
        _pacer_thread = threading.Thread(target=_pacer_probe)
        _pacer_thread.daemon = True
        _pacer_thread.start()
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(2) + " " + device
        )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(actual_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(comp, 0)
        self.osmosdr_source_0.set_iq_balance_mode(comp, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(irfgain, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna(antenna, 0)
        self.osmosdr_source_0.set_bandwidth(((int((samp_rate*0.8)) if bw == 0 else int(bw)) ), 0)
        self.osmosdr_source_0.set_center_freq(actual_freq, 1)
        self.osmosdr_source_0.set_freq_corr(0, 1)
        self.osmosdr_source_0.set_dc_offset_mode(comp, 1)
        self.osmosdr_source_0.set_iq_balance_mode(comp, 1)
        self.osmosdr_source_0.set_gain_mode(False, 1)
        self.osmosdr_source_0.set_gain(irfgain, 1)
        self.osmosdr_source_0.set_if_gain(0, 1)
        self.osmosdr_source_0.set_bb_gain(0, 1)
        self.osmosdr_source_0.set_antenna(antenna, 1)
        self.osmosdr_source_0.set_bandwidth(((int((samp_rate*0.8)) if bw == 0 else int(bw))), 1)
        self._ibaseline_tool_bar = Qt.QToolBar(self)
        self._ibaseline_tool_bar.addWidget(Qt.QLabel("Baseline Length" + ": "))
        self._ibaseline_line_edit = Qt.QLineEdit(str(self.ibaseline))
        self._ibaseline_tool_bar.addWidget(self._ibaseline_line_edit)
        self._ibaseline_line_edit.editingFinished.connect(
            lambda: self.set_ibaseline(eng_notation.str_to_num(str(self._ibaseline_line_edit.text()))))
        self.Main_grid_layout_3.addWidget(self._ibaseline_tool_bar, 2, 2, 1, 1)
        for r in range(2, 3):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(2, 3):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._iangWest_range = qtgui.Range(-180.0, 180.0, 2.0, angleWest, 400)
        self._iangWest_win = qtgui.RangeWidget(self._iangWest_range, self.set_iangWest, "Phase Correction West", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._iangWest_win, 4, 2, 1, 2)
        for r in range(4, 5):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(2, 4):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self._iangEast_range = qtgui.Range(-180.0, 180.0, 2.0, angleEast, 400)
        self._iangEast_win = qtgui.RangeWidget(self._iangEast_range, self.set_iangEast, "Phase Correction East", "counter_slider", float, QtCore.Qt.Horizontal)
        self.Main_grid_layout_3.addWidget(self._iangEast_win, 4, 0, 1, 2)
        for r in range(4, 5):
            self.Main_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 2):
            self.Main_grid_layout_3.setColumnStretch(c, 1)
        self.flipper_0 = flipper_0.blk(fftsize=fftsize, enabled=True if velocity != 0 else False)
        self.flipper = flipper.blk(fftsize=fftsize, enabled=True if velocity != 0 else False)
        self.fft_vxx_0_0 = fft.fft_vcc(fftsize, True, window.blackmanharris(fftsize), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, window.blackmanharris(fftsize), True, 1)
        self.blocks_sub_xx_1_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_1 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_cc(1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_patterned_interleaver_0 = blocks.patterned_interleaver(gr.sizeof_float*1, [0,1,2,3,4,5])
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, fftsize, (-20*math.log10(fftsize)-10*math.log10(winpower/fftsize)))
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, fftsize, (-20*math.log10(fftsize)-10*math.log10(winpower/fftsize)))
        self.blocks_multiply_const_xx_2 = blocks.multiply_const_ff(ihighpass, 1)
        self.blocks_multiply_const_xx_1_0 = blocks.multiply_const_cc(imulWest*phaseWest, 1)
        self.blocks_multiply_const_xx_1 = blocks.multiply_const_cc(imulEast*phaseEast, 1)
        self.blocks_multiply_const_xx_0_1 = blocks.multiply_const_ff((1.0/split_ratio)*dc_gain, 1)
        self.blocks_multiply_const_xx_0_0 = blocks.multiply_const_cc(1.0/split_ratio, 1)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff((1.0/split_ratio)*dc_gain, 1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(float(dc_gain*10))
        self.blocks_multiply_conjugate_cc_1 = blocks.multiply_conjugate_cc(1)
        self.blocks_keep_one_in_n_1_0 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, (int(fftrate/data_rate)))
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_float*fftsize, (int(fftrate/data_rate)))
        self.blocks_keep_one_in_n_0_2_0 = blocks.keep_one_in_n(gr.sizeof_float*1, (int(int(samp_rate/data_rate)/split_ratio)))
        self.blocks_keep_one_in_n_0_2 = blocks.keep_one_in_n(gr.sizeof_float*1, (int(int(samp_rate/data_rate)/split_ratio)))
        self.blocks_keep_one_in_n_0_1 = blocks.keep_one_in_n(gr.sizeof_float*1, (int(int(samp_rate/data_rate)/split_ratio)))
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, (int(int(samp_rate/data_rate)/split_ratio)))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, (int(int(samp_rate/data_rate)/split_ratio)))
        self.blocks_integrate_xx_0_1 = blocks.integrate_ff(split_ratio, 1)
        self.blocks_integrate_xx_0_0 = blocks.integrate_cc(split_ratio, 1)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(split_ratio, 1)
        self.blocks_complex_to_mag_squared_1_0 = blocks.complex_to_mag_squared(fftsize)
        self.blocks_complex_to_mag_squared_1 = blocks.complex_to_mag_squared(fftsize)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_1_0 = blocks.add_const_cc(idcwest)
        self.blocks_add_const_vxx_1 = blocks.add_const_cc(idceast)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff([1.0e-14]*fftsize if "file=" in device else [0.0]*fftsize)
        self.baseline_compensate_0 = baseline_compensate_0.blk(fftsize=fftsize, collect=True if correct_baseline == False else False)
        self.baseline_compensate = baseline_compensate.blk(fftsize=fftsize, collect=True if correct_baseline == False else False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.baseline_compensate, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.baseline_compensate_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.baseline_compensate_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_multiply_const_xx_1, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_multiply_const_xx_1_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.pacer_probe, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_patterned_interleaver_0, 2))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_patterned_interleaver_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.stripchart_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.stripchart_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_integrate_xx_0_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_1, 0), (self.single_pole_iir_filter_xx_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_1_0, 0), (self.single_pole_iir_filter_xx_1_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.single_pole_iir_filter_xx_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.single_pole_iir_filter_xx_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_1, 0), (self.blocks_multiply_const_xx_0_1, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_patterned_interleaver_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.stripchart, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_1, 0), (self.blocks_patterned_interleaver_0, 3))
        self.connect((self.blocks_keep_one_in_n_0_1, 0), (self.stripchart_1, 0))
        self.connect((self.blocks_keep_one_in_n_0_2, 0), (self.blocks_patterned_interleaver_0, 4))
        self.connect((self.blocks_keep_one_in_n_0_2, 0), (self.stripchart_1_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0, 0), (self.blocks_patterned_interleaver_0, 5))
        self.connect((self.blocks_keep_one_in_n_0_2_0, 0), (self.stripchart_1_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.baseline_compensate, 0))
        self.connect((self.blocks_keep_one_in_n_1_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_1, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_1, 0), (self.single_pole_iir_filter_xx_0_1, 0))
        self.connect((self.blocks_multiply_const_xx_1, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_multiply_const_xx_1, 0), (self.blocks_multiply_conjugate_cc_1, 0))
        self.connect((self.blocks_multiply_const_xx_1, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_multiply_const_xx_1_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_1_0, 0), (self.blocks_multiply_conjugate_cc_1, 1))
        self.connect((self.blocks_multiply_const_xx_1_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_2, 0), (self.blocks_sub_xx_1_0, 1))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.flipper, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.flipper_0, 0))
        self.connect((self.blocks_patterned_interleaver_0, 0), (self.formatter, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_const_xx_0_0, 0))
        self.connect((self.blocks_sub_xx_1, 0), (self.blocks_sub_xx_1_0, 0))
        self.connect((self.blocks_sub_xx_1, 0), (self.single_pole_iir_filter_xx_0_1_0, 0))
        self.connect((self.blocks_sub_xx_1_0, 0), (self.blocks_keep_one_in_n_0_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_1, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_complex_to_mag_squared_1_0, 0))
        self.connect((self.flipper, 0), (self.qtgui_vector_sink_f_1, 0))
        self.connect((self.flipper, 0), (self.vectorlogger, 0))
        self.connect((self.flipper_0, 0), (self.qtgui_vector_sink_f_1, 1))
        self.connect((self.flipper_0, 0), (self.vectorlogger_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.osmosdr_source_0, 1), (self.blocks_add_const_vxx_1_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_0_2, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_sub_xx_1, 0))
        self.connect((self.single_pole_iir_filter_xx_0_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.single_pole_iir_filter_xx_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.single_pole_iir_filter_xx_0_1, 0), (self.blocks_keep_one_in_n_0_2_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0_1, 0), (self.blocks_sub_xx_1, 1))
        self.connect((self.single_pole_iir_filter_xx_0_1_0, 0), (self.blocks_multiply_const_xx_2, 0))
        self.connect((self.single_pole_iir_filter_xx_1, 0), (self.blocks_keep_one_in_n_1, 0))
        self.connect((self.single_pole_iir_filter_xx_1_0, 0), (self.blocks_keep_one_in_n_1_0, 0))
        self.connect((self.stripchart, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.stripchart_0, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.stripchart_0_0, 0), (self.qtgui_vector_sink_f_0_0, 1))
        self.connect((self.stripchart_1, 0), (self.qtgui_vector_sink_f_0, 1))
        self.connect((self.stripchart_1_0, 0), (self.qtgui_vector_sink_f_0, 2))
        self.connect((self.stripchart_1_0_0, 0), (self.qtgui_vector_sink_f_0, 3))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "baa_seminar")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_angleEast(self):
        return self.angleEast

    def set_angleEast(self, angleEast):
        self.angleEast = angleEast
        self.set_iangEast(self.angleEast)

    def get_angleWest(self):
        return self.angleWest

    def set_angleWest(self, angleWest):
        self.angleWest = angleWest
        self.set_iangWest(self.angleWest)

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.osmosdr_source_0.set_antenna(self.antenna, 0)
        self.osmosdr_source_0.set_antenna(self.antenna, 1)

    def get_baseline(self):
        return self.baseline

    def set_baseline(self, baseline):
        self.baseline = baseline
        self.set_ibaseline(self.baseline)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.osmosdr_source_0.set_bandwidth(((int((self.samp_rate*0.8)) if self.bw == 0 else int(self.bw)) ), 0)
        self.osmosdr_source_0.set_bandwidth(((int((self.samp_rate*0.8)) if self.bw == 0 else int(self.bw))), 1)

    def get_comp(self):
        return self.comp

    def set_comp(self, comp):
        self.comp = comp
        self.osmosdr_source_0.set_dc_offset_mode(self.comp, 0)
        self.osmosdr_source_0.set_iq_balance_mode(self.comp, 0)
        self.osmosdr_source_0.set_dc_offset_mode(self.comp, 1)
        self.osmosdr_source_0.set_iq_balance_mode(self.comp, 1)

    def get_dceast(self):
        return self.dceast

    def set_dceast(self, dceast):
        self.dceast = dceast
        self.set_idceast(self.dceast)
        self.set_idcwest(self.dceast)

    def get_dcwest(self):
        return self.dcwest

    def set_dcwest(self, dcwest):
        self.dcwest = dcwest

    def get_declination(self):
        return self.declination

    def set_declination(self, declination):
        self.declination = declination
        self.set_idecln(self.declination)

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device
        self.set_is_usrp("uhd" in self.device)
        self.blocks_add_const_vxx_0.set_k([1.0e-14]*self.fftsize if "file=" in self.device else [0.0]*self.fftsize)

    def get_dmult(self):
        return self.dmult

    def set_dmult(self, dmult):
        self.dmult = dmult
        self.set_dc_gain(self.dmult)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_ifreq(self.freq)

    def get_highpass(self):
        return self.highpass

    def set_highpass(self, highpass):
        self.highpass = highpass
        self.set_ihighpass(self.highpass)

    def get_logtime(self):
        return self.logtime

    def set_logtime(self, logtime):
        self.logtime = logtime
        self.formatter.logtime = self.logtime
        self.vectorlogger.logtime = self.logtime*3
        self.vectorlogger_0.logtime = self.logtime*3

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude
        self.set_variable_qtgui_label_0(ra_funcs.cur_sidereal(self.longitude+self.tiktok).replace(",",":"))
        self.formatter.longitude = self.longitude
        self.vectorlogger.longitude = self.longitude
        self.vectorlogger_0.longitude = self.longitude

    def get_mulEast(self):
        return self.mulEast

    def set_mulEast(self, mulEast):
        self.mulEast = mulEast
        self.set_imulEast(self.mulEast)

    def get_mulWest(self):
        return self.mulWest

    def set_mulWest(self, mulWest):
        self.mulWest = mulWest
        self.set_imulWest(self.mulWest)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_variable_qtgui_label_0_0(self.prefix)
        self.formatter.filepat = self.prefix+'tp-%04d%02d%02d'
        self.vectorlogger.filepat = self.prefix+'fft-0-%04d%02d%02d'
        self.vectorlogger_0.filepat = self.prefix+'fft-1-%04d%02d%02d'

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.set_irfgain(self.rfgain)

    def get_seconds(self):
        return self.seconds

    def set_seconds(self, seconds):
        self.seconds = seconds

    def get_sinteg(self):
        return self.sinteg

    def set_sinteg(self, sinteg):
        self.sinteg = sinteg
        self.set_isinteg(self.sinteg)

    def get_srate(self):
        return self.srate

    def set_srate(self, srate):
        self.srate = srate
        self.set_samp_rate(int(self.srate))
        self.formatter.legend = "Sum,Corr(R),Corr(I),Diff,East,West,DEC=%f,FREQ=%f,BW=%f" % (self.idecln, self.ifreq/1.0e6, self.srate/1.0e6)

    def get_sync(self):
        return self.sync

    def set_sync(self, sync):
        self.sync = sync

    def get_tinteg(self):
        return self.tinteg

    def set_tinteg(self, tinteg):
        self.tinteg = tinteg
        self.set_itinteg(self.tinteg)

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title
        self.set_variable_qtgui_label_0_1(self.title + " " + self.today)

    def get_utc(self):
        return self.utc

    def set_utc(self, utc):
        self.utc = utc
        self.formatter.localtime = False if self.utc != 0 else True
        self.vectorlogger.localtime = False if self.utc != 0 else True
        self.vectorlogger_0.localtime = False if self.utc != 0 else True

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        self.flipper.enabled = True if self.velocity != 0 else False
        self.flipper_0.enabled = True if self.velocity != 0 else False
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if self.velocity == True else self.freqlow, ((self.dophigh-self.doplow)/self.fftsize if self.velocity == True else self.freqstep))
        self.qtgui_vector_sink_f_1.set_x_axis_units("km/s" if self.velocity == True else "MHz")

    def get_pacer(self):
        return self.pacer

    def set_pacer(self, pacer):
        self.pacer = pacer
        self.set_tiktok(self.pacer*0.0)

    def get_ifreq(self):
        return self.ifreq

    def set_ifreq(self, ifreq):
        self.ifreq = ifreq
        self.set_actual_freq(self.ifreq)
        self.set_dophigh(((self.samp_rate/2.0)/self.ifreq)*299792.0)
        self.set_doplow(-((self.samp_rate/2.0)/self.ifreq)*299792.0)
        self.set_fper(ra_funcs.fperiod(self.ifreq,self.ibaseline,self.idecln,0.0))
        self.set_freqlow((self.ifreq-(self.samp_rate/2.0))/1.0e6)
        Qt.QMetaObject.invokeMethod(self._ifreq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.ifreq)))
        self.set_tunereq(uhd.tune_request(self.ifreq,(self.samp_rate/2.0)+100e3))
        self.formatter.legend = "Sum,Corr(R),Corr(I),Diff,East,West,DEC=%f,FREQ=%f,BW=%f" % (self.idecln, self.ifreq/1.0e6, self.srate/1.0e6)

    def get_idecln(self):
        return self.idecln

    def set_idecln(self, idecln):
        self.idecln = idecln
        self.set_fper(ra_funcs.fperiod(self.ifreq,self.ibaseline,self.idecln,0.0))
        Qt.QMetaObject.invokeMethod(self._idecln_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.idecln)))
        self.formatter.legend = "Sum,Corr(R),Corr(I),Diff,East,West,DEC=%f,FREQ=%f,BW=%f" % (self.idecln, self.ifreq/1.0e6, self.srate/1.0e6)

    def get_ibaseline(self):
        return self.ibaseline

    def set_ibaseline(self, ibaseline):
        self.ibaseline = ibaseline
        self.set_fper(ra_funcs.fperiod(self.ifreq,self.ibaseline,self.idecln,0.0))
        Qt.QMetaObject.invokeMethod(self._ibaseline_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.ibaseline)))

    def get_gmt(self):
        return self.gmt

    def set_gmt(self, gmt):
        self.gmt = gmt

    def get_today(self):
        return self.today

    def set_today(self, today):
        self.today = today
        self.set_variable_qtgui_label_0_1(self.title + " " + self.today)

    def get_tiktok(self):
        return self.tiktok

    def set_tiktok(self, tiktok):
        self.tiktok = tiktok
        self.set_variable_qtgui_label_0(ra_funcs.cur_sidereal(self.longitude+self.tiktok).replace(",",":"))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_dophigh(((self.samp_rate/2.0)/self.ifreq)*299792.0)
        self.set_doplow(-((self.samp_rate/2.0)/self.ifreq)*299792.0)
        self.set_fftrate(int(self.samp_rate/self.fftsize))
        self.set_freqlow((self.ifreq-(self.samp_rate/2.0))/1.0e6)
        self.set_freqstep((self.samp_rate/self.fftsize)/1.0e6)
        self.set_tunereq(uhd.tune_request(self.ifreq,(self.samp_rate/2.0)+100e3))
        self.blocks_keep_one_in_n_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_1.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_2.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_2_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_bandwidth(((int((self.samp_rate*0.8)) if self.bw == 0 else int(self.bw)) ), 0)
        self.osmosdr_source_0.set_bandwidth(((int((self.samp_rate*0.8)) if self.bw == 0 else int(self.bw))), 1)
        self.single_pole_iir_filter_xx_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_0_0.set_taps((ra_funcs.getalpha(1.0/(self.fper*1.25),self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_1.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_1_0.set_taps((ra_funcs.getalpha(1.0/(self.fper*1.25),self.samp_rate/self.split_ratio)))

    def get_iangWest(self):
        return self.iangWest

    def set_iangWest(self, iangWest):
        self.iangWest = iangWest
        self.set_phaseWest(complex(math.cos(math.radians(self.iangWest)),math.sin(math.radians(self.iangWest))))

    def get_iangEast(self):
        return self.iangEast

    def set_iangEast(self, iangEast):
        self.iangEast = iangEast
        self.set_phaseEast(complex(math.cos(math.radians(self.iangEast)),math.sin(math.radians(self.iangEast))))

    def get_fper(self):
        return self.fper

    def set_fper(self, fper):
        self.fper = fper
        self.set_variable_qtgui_label_0_1_0("%5d secs" % self.fper)
        self.single_pole_iir_filter_xx_0_0_0.set_taps((ra_funcs.getalpha(1.0/(self.fper*1.25),self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_1_0.set_taps((ra_funcs.getalpha(1.0/(self.fper*1.25),self.samp_rate/self.split_ratio)))

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.set_fftrate(int(self.samp_rate/self.fftsize))
        self.set_freqstep((self.samp_rate/self.fftsize)/1.0e6)
        self.set_winpower(sum([x*x for x in window.blackman_harris(self.fftsize)]))
        self.blocks_add_const_vxx_0.set_k([1.0e-14]*self.fftsize if "file=" in self.device else [0.0]*self.fftsize)
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if self.velocity == True else self.freqlow, ((self.dophigh-self.doplow)/self.fftsize if self.velocity == True else self.freqstep))

    def get_winpower(self):
        return self.winpower

    def set_winpower(self, winpower):
        self.winpower = winpower

    def get_variable_qtgui_label_0_1_0(self):
        return self.variable_qtgui_label_0_1_0

    def set_variable_qtgui_label_0_1_0(self, variable_qtgui_label_0_1_0):
        self.variable_qtgui_label_0_1_0 = variable_qtgui_label_0_1_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_1_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_1_0_formatter(self.variable_qtgui_label_0_1_0))))

    def get_variable_qtgui_label_0_1(self):
        return self.variable_qtgui_label_0_1

    def set_variable_qtgui_label_0_1(self, variable_qtgui_label_0_1):
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_1_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_1_formatter(self.variable_qtgui_label_0_1))))

    def get_variable_qtgui_label_0_0(self):
        return self.variable_qtgui_label_0_0

    def set_variable_qtgui_label_0_0(self, variable_qtgui_label_0_0):
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_0_formatter(self.variable_qtgui_label_0_0))))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0))))

    def get_tunereq(self):
        return self.tunereq

    def set_tunereq(self, tunereq):
        self.tunereq = tunereq

    def get_split_ratio(self):
        return self.split_ratio

    def set_split_ratio(self, split_ratio):
        self.split_ratio = split_ratio
        self.blocks_keep_one_in_n_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_1.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_2.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_2_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_multiply_const_xx_0.set_k((1.0/self.split_ratio)*self.dc_gain)
        self.blocks_multiply_const_xx_0_0.set_k(1.0/self.split_ratio)
        self.blocks_multiply_const_xx_0_1.set_k((1.0/self.split_ratio)*self.dc_gain)
        self.single_pole_iir_filter_xx_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_0_0.set_taps((ra_funcs.getalpha(1.0/(self.fper*1.25),self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_1.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_1_0.set_taps((ra_funcs.getalpha(1.0/(self.fper*1.25),self.samp_rate/self.split_ratio)))

    def get_phaseWest(self):
        return self.phaseWest

    def set_phaseWest(self, phaseWest):
        self.phaseWest = phaseWest
        self.blocks_multiply_const_xx_1_0.set_k(self.imulWest*self.phaseWest)

    def get_phaseEast(self):
        return self.phaseEast

    def set_phaseEast(self, phaseEast):
        self.phaseEast = phaseEast
        self.blocks_multiply_const_xx_1.set_k(self.imulEast*self.phaseEast)

    def get_itinteg(self):
        return self.itinteg

    def set_itinteg(self, itinteg):
        self.itinteg = itinteg
        self.single_pole_iir_filter_xx_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_0.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))
        self.single_pole_iir_filter_xx_0_1.set_taps((ra_funcs.getalpha(1.0/self.itinteg,self.samp_rate/self.split_ratio)))

    def get_isinteg(self):
        return self.isinteg

    def set_isinteg(self, isinteg):
        self.isinteg = isinteg
        self.single_pole_iir_filter_xx_1.set_taps((ra_funcs.getalpha(1.0/self.isinteg,self.fftrate)))
        self.single_pole_iir_filter_xx_1_0.set_taps((ra_funcs.getalpha(1.0/self.isinteg,self.fftrate)))

    def get_is_usrp(self):
        return self.is_usrp

    def set_is_usrp(self, is_usrp):
        self.is_usrp = is_usrp

    def get_irfgain(self):
        return self.irfgain

    def set_irfgain(self, irfgain):
        self.irfgain = irfgain
        self.osmosdr_source_0.set_gain(self.irfgain, 0)
        self.osmosdr_source_0.set_gain(self.irfgain, 1)

    def get_imulWest(self):
        return self.imulWest

    def set_imulWest(self, imulWest):
        self.imulWest = imulWest
        self.blocks_multiply_const_xx_1_0.set_k(self.imulWest*self.phaseWest)

    def get_imulEast(self):
        return self.imulEast

    def set_imulEast(self, imulEast):
        self.imulEast = imulEast
        self.blocks_multiply_const_xx_1.set_k(self.imulEast*self.phaseEast)

    def get_ihighpass(self):
        return self.ihighpass

    def set_ihighpass(self, ihighpass):
        self.ihighpass = ihighpass
        self._ihighpass_callback(self.ihighpass)
        self.blocks_multiply_const_xx_2.set_k(self.ihighpass)

    def get_idcwest(self):
        return self.idcwest

    def set_idcwest(self, idcwest):
        self.idcwest = idcwest
        self.blocks_add_const_vxx_1_0.set_k(self.idcwest)

    def get_idceast(self):
        return self.idceast

    def set_idceast(self, idceast):
        self.idceast = idceast
        self.blocks_add_const_vxx_1.set_k(self.idceast)

    def get_freqstep(self):
        return self.freqstep

    def set_freqstep(self, freqstep):
        self.freqstep = freqstep
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if self.velocity == True else self.freqlow, ((self.dophigh-self.doplow)/self.fftsize if self.velocity == True else self.freqstep))

    def get_freqlow(self):
        return self.freqlow

    def set_freqlow(self, freqlow):
        self.freqlow = freqlow
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if self.velocity == True else self.freqlow, ((self.dophigh-self.doplow)/self.fftsize if self.velocity == True else self.freqstep))

    def get_fftrate(self):
        return self.fftrate

    def set_fftrate(self, fftrate):
        self.fftrate = fftrate
        self.blocks_keep_one_in_n_1.set_n((int(self.fftrate/self.data_rate)))
        self.blocks_keep_one_in_n_1_0.set_n((int(self.fftrate/self.data_rate)))
        self.single_pole_iir_filter_xx_1.set_taps((ra_funcs.getalpha(1.0/self.isinteg,self.fftrate)))
        self.single_pole_iir_filter_xx_1_0.set_taps((ra_funcs.getalpha(1.0/self.isinteg,self.fftrate)))

    def get_doplow(self):
        return self.doplow

    def set_doplow(self, doplow):
        self.doplow = doplow
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if self.velocity == True else self.freqlow, ((self.dophigh-self.doplow)/self.fftsize if self.velocity == True else self.freqstep))

    def get_dophigh(self):
        return self.dophigh

    def set_dophigh(self, dophigh):
        self.dophigh = dophigh
        self.qtgui_vector_sink_f_1.set_x_axis(self.doplow if self.velocity == True else self.freqlow, ((self.dophigh-self.doplow)/self.fftsize if self.velocity == True else self.freqstep))

    def get_dc_gain(self):
        return self.dc_gain

    def set_dc_gain(self, dc_gain):
        self.dc_gain = dc_gain
        self.blocks_multiply_const_vxx_0_0.set_k(float(self.dc_gain*10))
        self.blocks_multiply_const_xx_0.set_k((1.0/self.split_ratio)*self.dc_gain)
        self.blocks_multiply_const_xx_0_1.set_k((1.0/self.split_ratio)*self.dc_gain)

    def get_data_rate(self):
        return self.data_rate

    def set_data_rate(self, data_rate):
        self.data_rate = data_rate
        self.blocks_keep_one_in_n_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_1.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_2.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_0_2_0.set_n((int(int(self.samp_rate/self.data_rate)/self.split_ratio)))
        self.blocks_keep_one_in_n_1.set_n((int(self.fftrate/self.data_rate)))
        self.blocks_keep_one_in_n_1_0.set_n((int(self.fftrate/self.data_rate)))
        self.qtgui_vector_sink_f_1.set_update_time((1.0/(self.data_rate)))
        self.stripchart.decim = self.data_rate
        self.stripchart_0.decim = self.data_rate
        self.stripchart_0_0.decim = self.data_rate
        self.stripchart_1.decim = self.data_rate
        self.stripchart_1_0.decim = self.data_rate
        self.stripchart_1_0_0.decim = self.data_rate

    def get_correct_baseline(self):
        return self.correct_baseline

    def set_correct_baseline(self, correct_baseline):
        self.correct_baseline = correct_baseline
        self._correct_baseline_callback(self.correct_baseline)
        self.baseline_compensate.collect = True if self.correct_baseline == False else False
        self.baseline_compensate_0.collect = True if self.correct_baseline == False else False

    def get_actual_freq(self):
        return self.actual_freq

    def set_actual_freq(self, actual_freq):
        self.actual_freq = actual_freq
        self.osmosdr_source_0.set_center_freq(self.actual_freq, 0)
        self.osmosdr_source_0.set_center_freq(self.actual_freq, 1)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--angleEast", dest="angleEast", type=eng_float, default=eng_notation.num_to_str(float(0.0)),
        help="Set Phase Corr. Angle EAST [default=%(default)r]")
    parser.add_argument(
        "--angleWest", dest="angleWest", type=eng_float, default=eng_notation.num_to_str(float(0.0)),
        help="Set Phase Corr. Angle WEST [default=%(default)r]")
    parser.add_argument(
        "--antenna", dest="antenna", type=str, default="",
        help="Set Antenna Selection [default=%(default)r]")
    parser.add_argument(
        "--baseline", dest="baseline", type=eng_float, default=eng_notation.num_to_str(float(4.0)),
        help="Set Interferometer Baseline (meters) [default=%(default)r]")
    parser.add_argument(
        "--bw", dest="bw", type=eng_float, default=eng_notation.num_to_str(float(0.0)),
        help="Set Analog Bandwidth [default=%(default)r]")
    parser.add_argument(
        "--comp", dest="comp", type=intx, default=0,
        help="Set DC/IQ compensation mode [default=%(default)r]")
    parser.add_argument(
        "--dceast", dest="dceast", type=eng_float, default=eng_notation.num_to_str(float(0.0)),
        help="Set East DC correction [default=%(default)r]")
    parser.add_argument(
        "--dcwest", dest="dcwest", type=eng_float, default=eng_notation.num_to_str(float(0.0)),
        help="Set West DC Correction [default=%(default)r]")
    parser.add_argument(
        "--declination", dest="declination", type=eng_float, default=eng_notation.num_to_str(float(45.0)),
        help="Set Object Declination [default=%(default)r]")
    parser.add_argument(
        "--device", dest="device", type=str, default="rtl=0 rlt=1",
        help="Set Device string [default=%(default)r]")
    parser.add_argument(
        "--dmult", dest="dmult", type=eng_float, default=eng_notation.num_to_str(float(1)),
        help="Set Detector Multiplier [default=%(default)r]")
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default=eng_notation.num_to_str(float(1420.4058e6)),
        help="Set RF Frequency (Hz) [default=%(default)r]")
    parser.add_argument(
        "--highpass", dest="highpass", type=intx, default=0,
        help="Set HIgh pass for differential pathway [default=%(default)r]")
    parser.add_argument(
        "--logtime", dest="logtime", type=eng_float, default=eng_notation.num_to_str(float(5.0)),
        help="Set Logging Interval (secs) [default=%(default)r]")
    parser.add_argument(
        "--longitude", dest="longitude", type=eng_float, default=eng_notation.num_to_str(float((-76.03))),
        help="Set Longitude [default=%(default)r]")
    parser.add_argument(
        "--mulEast", dest="mulEast", type=eng_float, default=eng_notation.num_to_str(float(1.0)),
        help="Set A channel balance multiplier [default=%(default)r]")
    parser.add_argument(
        "--mulWest", dest="mulWest", type=eng_float, default=eng_notation.num_to_str(float(1.0)),
        help="Set B channel balance multiplier [default=%(default)r]")
    parser.add_argument(
        "--prefix", dest="prefix", type=str, default="./",
        help="Set File prefix [default=%(default)r]")
    parser.add_argument(
        "--rfgain", dest="rfgain", type=eng_float, default=eng_notation.num_to_str(float(40)),
        help="Set RF Gain (dB) [default=%(default)r]")
    parser.add_argument(
        "--seconds", dest="seconds", type=intx, default=3600,
        help="Set Strip chart length, seconds [default=%(default)r]")
    parser.add_argument(
        "--sinteg", dest="sinteg", type=eng_float, default=eng_notation.num_to_str(float(10.0)),
        help="Set Integraton Time(secs) for Spectrum [default=%(default)r]")
    parser.add_argument(
        "--srate", dest="srate", type=eng_float, default=eng_notation.num_to_str(float(2.56e6)),
        help="Set Sample Rate (SPS) [default=%(default)r]")
    parser.add_argument(
        "--sync", dest="sync", type=intx, default=0,
        help="Set Enable PPS sync [default=%(default)r]")
    parser.add_argument(
        "--tinteg", dest="tinteg", type=eng_float, default=eng_notation.num_to_str(float(45)),
        help="Set Integraton Time(secs) for TP [default=%(default)r]")
    parser.add_argument(
        "--title", dest="title", type=str, default="BAA Seminar",
        help="Set Title [default=%(default)r]")
    parser.add_argument(
        "--utc", dest="utc", type=intx, default=1,
        help="Set Log in UTC time [default=%(default)r]")
    parser.add_argument(
        "--velocity", dest="velocity", type=intx, default=1,
        help="Set Show velocities [default=%(default)r]")
    return parser


def main(top_block_cls=baa_seminar, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(angleEast=options.angleEast, angleWest=options.angleWest, antenna=options.antenna, baseline=options.baseline, bw=options.bw, comp=options.comp, dceast=options.dceast, dcwest=options.dcwest, declination=options.declination, device=options.device, dmult=options.dmult, freq=options.freq, highpass=options.highpass, logtime=options.logtime, longitude=options.longitude, mulEast=options.mulEast, mulWest=options.mulWest, prefix=options.prefix, rfgain=options.rfgain, seconds=options.seconds, sinteg=options.sinteg, srate=options.srate, sync=options.sync, tinteg=options.tinteg, title=options.title, utc=options.utc, velocity=options.velocity)
    snippets_main_after_init(tb)
    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
