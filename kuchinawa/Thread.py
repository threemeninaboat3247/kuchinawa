# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 00:56:52 2017

@author: Yuki
"""
import sys

from multiprocessing import Queue,Process
from abc import abstractmethod

from PyQt5.QtCore import pyqtSignal,QThread
from PyQt5.QtWidgets import QToolBar,QAction,QMainWindow,QWidget,QApplication,\
                            QScrollArea,QFileDialog,QDesktopWidget
from PyQt5.QtGui import QIcon                        

from kuchinawa import Graph,File
import kuchinawa

class MyToolBar(QToolBar):
    '''
    A toolbar which has several states. Each state has specific executable actions.
    '''
    READY=0     #a flag which means the program is ready to start
    RUNNING=1   #the program is running
    
    def __init__(self):
        super().__init__()
        self.exeAction=QAction('Run', self)
        self.stopAction = QAction('Stop', self)
        self.debugAction = QAction('Debug', self)
        self.exitAction=QAction('Exit',self)
        self.addAction(self.exeAction)
        self.addAction(self.stopAction)
        self.addAction(self.debugAction)
        self.addAction(self.exitAction)
        
    def setState(self,end):
        '''change the current state'''
        if end==MyToolBar.READY:
            self.exeAction.setEnabled(True)
            self.stopAction.setEnabled(False)
            self.debugAction.setEnabled(True)
            self.exitAction.setEnabled(True)
        elif end==MyToolBar.RUNNING:
            self.exeAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.debugAction.setEnabled(False)
            self.exitAction.setEnabled(True)
            

class Main(QThread):
    '''
    A base class for measurement programs. Users can make a measurement program by inheriting this class.
    '''
    
    __callSignal=pyqtSignal(object,tuple,dict)
    
    def __init__(self):
        super().__init__()
        self.__initUI()
        self.finished.connect(self.__finalize)
        self.running=False #a flag which determins whether run method ends or not
        
        self.que=Queue() #connect between main and graph drawing process
        self.p=Process(target=Graph.initGraphContainer,args=(self.que,))
        self.p.start()
        
        self.result=Queue() #queue to put a result of a function called in the thread in which itself exists
        self.__callSignal.connect(self.__call)
        
        #place the window to the left of the screen
        screen=QDesktopWidget().availableGeometry()
        height=screen.height()
        width=screen.width()/2
        self.mw.setGeometry(0,40,width,height)
        self.mw.setWindowIcon(QIcon(kuchinawa.ICONPATH))
        self.mw.setWindowTitle(kuchinawa.KUCHINAWA+' Control Panel')
        self.mw.show()
        
    
    def __initUI(self):
        self.mw=QMainWindow()
        self.scroll=QScrollArea()
        self.mw.setCentralWidget(self.scroll)
        
        self.toolbar=MyToolBar()
        self.toolbar.exeAction.triggered.connect(self.__exePressed)
        self.toolbar.stopAction.triggered.connect(self.__stopPressed)
        self.toolbar.exitAction.triggered.connect(self.__exitPressed)
        self.toolbar.setState(MyToolBar.READY)
        self.mw.addToolBar(self.toolbar)
        
    def setUI(self,ui):
        '''
        Set a user interface made by qtdesigner to the MainWindow.
        
        Parameters:
            ui: UI_Form
            
        Returns:
            None
        
        '''
        self.widget=QWidget()
        ui.setupUi(self.widget)
        self.scroll.setWidget(self.widget)
        
    @abstractmethod    
    def run(self):
        '''
        The body of a measurement program. Users implement this method for their measurement.
        '''
        raise NotImplementedError('This method must be implemented in a subclass.')
            
    def __exePressed(self):
        self.toolbar.setState(MyToolBar.RUNNING)
        self.__resetGraphs()
        self.running=True
        self.start()
        
    def __exitPressed(self):
        self.__stopPressed()
        self.que.put(Graph.PoisonPill())
        del(self.mw)
        
    def __stopPressed(self):
        self.running=False
        
    def __finalize(self):
        self.toolbar.setState(MyToolBar.READY)
        self.running=False
        
    def call(self,function,args=None,kwargs=None):
        '''
        Call a function in the thread in which the instance of this class exists.
        
        Paramters:
            function: function
                a function to call
            args: tuple
                positional arguments
            kwargs: dict
                keyward arguments
                
        Returns:
            object
                depends on the function
        '''
        if args==None:
            args=()
        if kwargs==None:
            kwargs={}
        self.__callSignal.emit(function,args,kwargs)
        result=self.result.get()
        return result
        
    def __call(self,function,args=None,kwargs=None):
        '''
        A slot method for __callSignal. This method is executed when __callSignal is emit and put the return to self.result.
        '''
        if args==None:
            args=()
        if kwargs==None:
            kwargs={}
        result=function(*args,**kwargs)
        self.result.put(result)
        
    def addGraph(self,graph,args=None,kwargs=None,name='Unnamed'):
        '''
        Add a graph to GraphContainer.
        
        Parameters:
            graph: class
                a subclass of Graph.GraphBase
            *args: tuple
                positional arguments to pass to __init__ of 'graph'
            **kwargs: dict
                keyword arguments to pass to __init__ of 'graph'
            name: string
                the window title of the graph
        Returns: Graph.GraphInterface
            the interface to plot data to the graph
        '''
        if args==None:
            args=()
        if kwargs==None:
            kwargs={}
        interface=Graph.GraphInterface(self.que,graph,name,*args,**kwargs)
        return interface
        
    def __resetGraphs(self):
        '''
        Reset GraphContainer.
        
        Parameters:
            None
        Returns:
            None
        '''
        self.que.put(Graph.ResetSignal())
        
    def getSaveFile(self,sep='\t',comment='#'):
        '''
        Open a file dialog and return a csv file instance holding the path appointed in the dialog.
        
        Parameters:
            sep: str
                the seperater between values in the csv file
            comment: str
                the header of comment lines
        Returns:
            File.File
        '''
        def fileDialog(parent):
            path,hoge = QFileDialog.getSaveFileName(parent, 'select a file to write data to')
            return path
        path=self.call(fileDialog,(self.mw,))
        file=File.File(path)
        return file

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    t=Main()
    sys.exit(app.exec_())