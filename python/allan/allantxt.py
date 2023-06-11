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
from time import time
############# graphics part

class allan(gr.sync_block):
    """
    docstring for block allan
    """
    def __init__(self, allan_type=0):
        gr.sync_block.__init__(self,
            name="allan",
            in_sig=[numpy.float32],
            out_sig=None)
        self.counter=0
        self.allan_type=allan_type
        print("Init",flush=True)
        self.dev_rt = at.realtime.tdev_realtime(tau0=1.0,auto_afs=True)
        if allan_type==0:
            self.dev_rt = at.realtime.tdev_realtime(tau0=1.0,auto_afs=True)
        if allan_type==1:
            self.dev_rt = at.realtime.ohdev_realtime(tau0=1.0,auto_afs=True)
        if allan_type==2:
            self.dev_rt = at.realtime.oadev_realtime(tau0=1.0,auto_afs=True)
        self.single=True   # update a single trace (True) or accumulate traces (False)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        # signal processing here
        for x in in0:
            self.counter=self.counter+1
            self.dev_rt.add_phase(x)
            taus=self.dev_rt.taus()
            devs=self.dev_rt.devs()
            if (self.counter>1000):
                print(self.counter,flush=True)
                self.counter=0
                print(taus)
                print(devs)
        return len(input_items[0])
