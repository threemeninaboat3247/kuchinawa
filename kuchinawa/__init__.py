# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 03:24:37 2017

@author: Yuki
"""
from kuchinawa.Compile import compileUi
from kuchinawa.Thread import Main

ENTRYPOINT=__path__[0]
ICONPATH=ENTRYPOINT+'\\Icons\\logo.png'
KUCHINAWA='Kuchinawa'

def run_sample():
    from PyQt5.QtWidgets import QApplication
    import sys
    from kuchinawa.Examples import SinCos
    app = QApplication([])
    s=SinCos.Sample()
    sys.exit(app.exec_())    
