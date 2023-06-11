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
        if (len(plottaus)>1):
            tausmax=numpy.log10(max(plottaus))
            devsmax=numpy.log10(max(plotdevs))
            devsmin=numpy.log10(min(plotdevs))
            path = QPainterPath()
            path.moveTo(numpy.log10(plottaus[0])/tausmax*self.width(), self.height()-(numpy.log10(plotdevs[0])-devsmin)/(devsmax-devsmin)*self.height())
            for n in range(len(plottaus[1:-1])): # starts counting at 0
               path.lineTo(numpy.log10(plottaus[n+1])/tausmax*self.width(), self.height()-(numpy.log10(plotdevs[n+1])-devsmin)/(devsmax-devsmin)*self.height())
            painter.drawPath(path)
            painter.drawText(5, 15, str(max(plotdevs)))
            painter.drawText(5, self.height()-5, str(min(plotdevs)))
            painter.drawText(self.width()-75, self.height()-5, str(max(plottaus))) 
            
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
    def __init__(self, allan_type=0, input_type=False, allan_inc=1000, textdisplay=False, backgroundColor='white', parent=None):
        gr.sync_block.__init__(self,
            name="allan",
            in_sig=[numpy.float32],
            out_sig=None)
        self.counter=0
        self.allan_type=allan_type
        self.allan_inc=allan_inc
        self.textdisplay=textdisplay
        self.input_type=input_type
        print("Init "+str(allan_type),flush=True)
        self.dev_rt = at.realtime.tdev_realtime(tau0=1.0,auto_afs=True)  # default
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
            if self.input_type==False:
                self.dev_rt.add_frequency(x)
            else:
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
