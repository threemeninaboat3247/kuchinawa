# -*- coding: utf-8 -*-

""" --- Description ---
    Module:
        Template.py
    Abstract:
        The template file for users.
    Modified:
        threemeninaboat3247 2018/04/30
    ---    End      ---
"""
# Standard library imports
import sys,time
from datetime import datetime

# Third party library imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
import numpy as np

# Local imports
from kuchinawa.Thread import Main
from kuchinawa import Graph

class Sample(Main):
    def __init__(self):
        super().__init__()
        
    def run(self):
        # Initialization
        
        while self.running==True:
            # Loop process
            pass
        
        # Finalization

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s=Sample()
    sys.exit(app.exec_())       