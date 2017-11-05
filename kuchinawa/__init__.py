# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 03:24:37 2017

@author: Yuki
"""
import os,sys

from kuchinawa.Compile import compileUi
from kuchinawa.Thread import Main

import pdb
pdb.set_trace()
ENTRYPOINT=__path__[0]
ICONPATH=os.path.join(ENTRYPOINT,'Icons','logo.png')
KUCHINAWA='Kuchinawa'

#change the multiprocessing's context to 'spawn'
try:
    import multiprocessing
    multiprocessing.set_start_method('spawn')
except:
    print('The context of multiprocessing is already set.')

def run_sample():
    '''Run a sample program'''
    from PyQt5.QtWidgets import QApplication
    from kuchinawa.Examples import SinCos
    app = QApplication([])
    s=SinCos.Sample()
    sys.exit(app.exec_())
