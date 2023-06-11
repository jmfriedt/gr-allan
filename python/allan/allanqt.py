#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 JM Friedt.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import allantools as at
import numpy
from gnuradio import gr
############# graphics part
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget, QApplication, QLabel

class AllanAff(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.taus=[0.]
        self.devs=[0.]
        self.show()
        self.resize(600, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()
        print(len(self.taus))
#        print(self.devs)
        if self.devs[-1]==0:
            plottaus=self.taus[0:-2]
            plotdevs=self.devs[0:-2]
        else:
            plottaus=self.taus
            plotdevs=self.devs
        if (len(plottaus)>0):
            tausmax=numpy.log10(max(plottaus))
            devsmax=numpy.log10(max(plotdevs))
            devsmin=numpy.log10(min(plotdevs))
            path = QPainterPath()
            for n in range(len(plottaus)):
                path.lineTo(numpy.log10(plottaus[n])/tausmax*self.width(), (numpy.log10(plotdevs[n])-devsmin)/(devsmax-devsmin)*self.height())
            painter.drawPath(path)

    def setValue(self, taus,devs):
#        print("New QWidget value")
        self.taus=taus
        self.devs=devs
        self.update()
############################

class allan(gr.sync_block, AllanAff): # Display):
    """
    docstring for block allan
    """
    def __init__(self, allan_type=0, allan_inc=1000, textdisplay=False, backgroundColor='white', parent=None):
        gr.sync_block.__init__(self,
            name="allan",
            in_sig=[numpy.float32],
            out_sig=None)
        self.counter=0
        self.allan_type=allan_type
        self.allan_inc=allan_inc
        self.textdisplay=textdisplay
        print("Init "+str(allan_type),flush=True)
        self.dev_rt = at.realtime.tdev_realtime(tau0=1.0,auto_afs=True)
        if allan_type==0:
            self.dev_rt = at.realtime.tdev_realtime(tau0=1.0,auto_afs=True)
        if allan_type==1:
            self.dev_rt = at.realtime.ohdev_realtime(tau0=1.0,auto_afs=True)
        if allan_type==2:
            self.dev_rt = at.realtime.oadev_realtime(tau0=1.0,auto_afs=True)
#### graphics part   
        self.affichage=AllanAff.__init__(self,parent)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        # signal processing here
        for x in in0:
            self.counter=self.counter+1
            self.dev_rt.add_phase(x)
            if (self.counter>self.allan_inc):
                self.counter=0
                taus=self.dev_rt.taus()
                devs=self.dev_rt.devs()
                if (self.textdisplay==True):
                    print(taus)
                    print(devs)
                super().setValue(taus,devs)
        return len(input_items[0])

    def setValue(self, taus,devs):
        super().setValue(taus,devs)
