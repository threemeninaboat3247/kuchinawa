# -*- coding: utf-8 -*-
import sys,time
from datetime import datetime

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor

import numpy as np

from kuchinawa.Thread import Main
from kuchinawa import Graph

class Sample(Main):
    def __init__(self):
        super().__init__()
        
    def run(self):
        #Initialization
        
        while self.running==True:
            #Loop process
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s=Sample()
    sys.exit(app.exec_())       