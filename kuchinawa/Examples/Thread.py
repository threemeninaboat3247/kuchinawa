# -*- coding: utf-8 -*-
import multiprocessing
import sys,time
from datetime import datetime

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QThread

import numpy as np

from kuchinawa.Thread import Main
from kuchinawa import Graph

import Thread_ui

class MyThread(QThread):
    def __init__(self,call,lcd,progress,stop_signal,graph):
        super().__init__()
        self.call=call
        self.lcd=lcd
        self.progress=progress
        stop_signal.connect(self.stop)
        self.graph=graph
        self.run=True
        
    def run(self):
        timeOrigin=datetime.now() #get the origin of time
        self.run=True
        while self.run:
            time.sleep(0.01)
            t=(datetime.now()-timeOrigin).total_seconds()
            r=np.random.rand()
            self.call(self.lcd.display,(r,))
            self.graph.put({'x':t,'y':r})
        
    def stop(self):
        self.run=False
        print('stop')
        
T='Time'
V='Value'
COLORS=[QColor(255,0,0),QColor(255,255,0),QColor(0,255,0)] #the colors of points in graphs

class Sample(Main):
    def __init__(self):
        super().__init__()
        self.ui=Thread_ui.Ui_Form()
        self.setUI(self.ui)
        self.g1=self.addGraph(Graph.ScatterAll,(T,'sec',V,'V'),{'color':COLORS[0]},'Thread1')
        self.g2=self.addGraph(Graph.ScatterAll,(T,'sec',V,'V'),{'color':COLORS[1]},'Thread2')
        self.g3=self.addGraph(Graph.ScatterAll,(T,'sec',V,'V'),{'color':COLORS[2]},'Thread3')
        self.t1=MyThread(self.call,self.ui.lcd1,self.ui.bar1,self.ui.button1.pressed,self.g1)
        self.t2=MyThread(self.call,self.ui.lcd2,self.ui.bar2,self.ui.button2.pressed,self.g2)
        self.t3=MyThread(self.call,self.ui.lcd3,self.ui.bar3,self.ui.button3.pressed,self.g3)
        
    def run(self):
        self.t1.start()
        self.t2.start()
        self.t3.start()
        
        self.t1.wait()
        self.t2.wait()
        self.t3.wait()
        print('hoge')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s=Sample()
    sys.exit(app.exec_())       