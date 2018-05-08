# -*- coding: utf-8 -*-

""" --- Description ---
    Module:
        Thread.py
    Abstract:
        This module deals with classes which provide users the base for coding.
    Modified:
        threemeninaboat3247 2018/04/30
    ---    End      ---
"""
# Standard library imports
import sys
from multiprocessing import Queue,Process
from abc import abstractmethod

# Third party library imports
from PyQt5.QtCore import pyqtSignal,QThread
from PyQt5.QtWidgets import QToolBar,QAction,QMainWindow,QWidget,QApplication,\
                            QScrollArea,QFileDialog,QDesktopWidget
from PyQt5.QtGui import QIcon                        

# Local imports
from kuchinawa import Graph,File,Setting_extend
import kuchinawa

class MyToolBar(QToolBar):
    '''
    A toolbar which has several states. Each state has specific executable actions.
    '''
    READY=0     # A constant value which means the program is ready to start
    RUNNING=1   # A constant value which means the program is running
    
    def __init__(self):
        super().__init__()
        self.exeAction=QAction('Run', self)
        self.stopAction = QAction('Stop', self)
        self.debugAction = QAction('Debug', self)
        self.settingAction=QAction('Settings',self)
        self.exitAction=QAction('Exit',self)
        self.addAction(self.exeAction)
        self.addAction(self.stopAction)
        self.addAction(self.debugAction)
        self.addAction(self.settingAction)
        self.addAction(self.exitAction)
        
    def setState(self,end):
        '''change the current state'''
        if end==MyToolBar.READY:
            self.exeAction.setEnabled(True)
            self.stopAction.setEnabled(False)
            self.debugAction.setEnabled(True)
            self.settingAction.setEnabled(True)
            self.exitAction.setEnabled(True)
        elif end==MyToolBar.RUNNING:
            self.exeAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.debugAction.setEnabled(False)
            self.settingAction.setEnabled(True)
            self.exitAction.setEnabled(True)
            

class Main(QThread):
    '''
    A base class for measurement programs. Users can make a measurement program by inheriting this class.
    
    Notes:
         This class has a graphical user interface which includes a toolbar and the widget made by a user.
        Here, we call the thread where this class's instance lives 'main' thread.
        The user's code is to be written in 'run' method and executed in another thread. We call this one 'run' thread.
        
         Usually, we cannot call a function of a widget in another thread from other thread. 
        To realize this, we use pyqtSignal and Queue object. 
        When a user want to get a value of a widget of GUI in 'run' thread, they need to call 'call' method, handing out 
        the widget and arguments. Then, '__callSignal' is emitted and '__call' method is triggered in 'main' thread. The 
        result of the function is pushed to 'result' queue by 'main' thread. This result is popped by 'run' thread and 
        finally returned as the return value of 'call' method.
        
    Refs:
        ~/overview.png
    '''
    
    __callSignal=pyqtSignal(object,tuple,dict) # Emitted when a user call a function of a widget by 'call' method
    
    def __init__(self):
        super().__init__()
        
        # Declaration of instance variables
        self.__initUI() # Make user interface. Instance variables are declared in this method too
        self.que=Queue() # Connect between main and graph drawing process
        self.p=Process(target=Graph.initGraphContainer,args=(self.que,)) # Graph drawing process
        self.result=Queue() # Queue to put a result of a function called in the thread in which itself exists
        
        self.finished.connect(self.__finalize)
        self.__callSignal.connect(self.__call)
        
        self.running=False # Flag which determins whether run method is still running or not
        self.p.start()
   
    def __initUI(self):
        # Make the main window
        self.mw=QMainWindow()
        self.scroll=QScrollArea()
        self.mw.setCentralWidget(self.scroll)
        
        self.toolbar=MyToolBar()
        self.toolbar.exeAction.triggered.connect(self.__exePressed)
        self.toolbar.stopAction.triggered.connect(self.__stopPressed)
        self.toolbar.exitAction.triggered.connect(self.__exitPressed)
        self.toolbar.settingAction.triggered.connect(self.__settingPressed)
        self.toolbar.setState(MyToolBar.READY)
        self.mw.addToolBar(self.toolbar)
        
        #place the window to the left of the screen
        screen=QDesktopWidget().availableGeometry()
        height=screen.height()
        width=screen.width()/2
        self.mw.setGeometry(0,40,width,height)
        self.mw.setWindowIcon(QIcon(kuchinawa.ICONPATH))
        self.mw.setWindowTitle(kuchinawa.KUCHINAWA+' Control Panel')
        self.mw.show()
        
    def setUI(self,ui):
        '''
        Set a user interface made by QtDesigner to the main window.
        
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
        The body of a measurement program. Users need to implement this method for their measurements.
        '''
        raise NotImplementedError('This method must be implemented in a subclass.')
            
    def __exePressed(self):
        # Called when 'exe' button is pressed
        self.toolbar.setState(MyToolBar.RUNNING)
        self.__resetGraphs()
        self.running=True
        self.start()
        
    def __exitPressed(self):
        # Called when 'exit' button is pressed
        self.__stopPressed()
        self.que.put(Graph.PoisonPill())
        del(self.mw)
        
    def __settingPressed(self):
        # Called when 'setting' button is pressed
        try:
            self.settingWindow.showNormal()
        except:
            self.settingWindow=QWidget()
            self.settingUi=Setting_extend.My_Ui_Form()
            self.settingUi.setupUi(self.settingWindow)
            self.settingUi.make_interface()
            self.settingWindow.show()
        
    def __stopPressed(self):
        # Called when 'stop' button is pressed
        self.running=False
        
    def __finalize(self):
        # Called when 'run' method is finished
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