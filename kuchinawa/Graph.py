# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 20:32:27 2017

@author: Yuki
"""
import sys,threading

from abc import abstractmethod
import multiprocessing
from multiprocessing import Process,Queue

from PyQt5.QtWidgets import QApplication,QMainWindow,QDockWidget,QDesktopWidget
from PyQt5.QtCore import pyqtSignal,Qt,QThread,QTimer
from PyQt5.QtGui import QIcon
import pyqtgraph as pg

import kuchinawa

class AddSignal:
    '''
    A class which capsule information to instantiate a graph in another process.
    '''
    def __init__(self,identifier,graph,name,*args,**kwargs):
        self.identifier=identifier
        self.graph=graph
        self.name=name
        self.args=args
        self.kwargs=kwargs
        
class RemoveSignal:
    '''
    A class which capsule information to remove a graph in another process.
    '''
    def __init__(self,identifier):
        self.identifier=identifier
        
class DataSignal:
    '''
    A class which capsule data to plot onto a graph in another process.
    '''
    def __init__(self,identifier,data):
        self.identifier=identifier
        self.data=data

class ResetSignal:
    '''
    The instance of this class resets GraphContainer.
    '''
    pass

class PoisonPill:
    '''
    The instance of this class kills GraphContainer.
    '''
    pass
        
class GraphInterface:
    '''
    A interface to plot data onto a graph in another process. An instance of this class holds Queue connected to GraphContainer.
    '''
    Total=0
    def __init__(self,que,graph,name,*args,**kwargs):
        self.que=que
        self.identifier=GraphInterface.Total
        self.que.put(AddSignal(self.identifier,graph,name,*args,**kwargs))
        GraphInterface.Total+=1
        
    def put(self,data):
        '''
        Put data to the Queue connected to the graph
        
        Parameters:
            data: object
                Any object can be given. It depends on the implementation of the graph class how the data is treated
        '''
        identified_data=DataSignal(self.identifier,data)
        self.que.put(identified_data)
        
    def remove(self):
        self.que.put(RemoveSignal(self.identifier))
        
class watchQue(QThread):
    addSignal=pyqtSignal(int,object,str,tuple,dict)
    dataSignal=pyqtSignal(int,object)
    resetSignal=pyqtSignal()
    removeSignal=pyqtSignal(int)
    poisonSignal=pyqtSignal()
    
    def __init__(self,que,gc):
        super().__init__()
        self.que=que 
        self.gc=gc #GraphContainer
        self.stop_event=threading.Event()
        
    def run(self):
        while not self.stop_event.is_set():
            signal=self.que.get()
            if isinstance(signal,DataSignal):
                self.dataSignal.emit(signal.identifier,signal.data)
            elif isinstance(signal,AddSignal):
                self.addSignal.emit(signal.identifier,signal.graph,signal.name,signal.args,signal.kwargs)
            elif isinstance(signal,RemoveSignal):
                self.removeSignal.emit(signal.identifier)
            elif isinstance(signal,ResetSignal):
                self.resetSignal.emit()
            elif isinstance(signal,PoisonPill):
                self.poisonSignal.emit()
                self.stop()

    def stop(self):
        self.stop_event.set()
        
class DockList:
    '''
    A list of QDockWidgets holds a index. The QDockWidgets at the index or later have no child.
    '''
    def __init__(self):
        self.docks=[]
        self.index=None #None means all the QDockWidgets have a child
    
    def setWidget(self,widget,name):
        '''
        Set a widget to the QDockWidget which has no child at the minimum index.
        
        Parameters:
            widget: pg.PlotWidget
                a widget to add
            name: str
                the window title of the QDockWidget
        Returns:
            (bool,QDockWidget)
                bool: True if generated a new QDockWidget
                QDockWidget: the QDockWidget to which the widget was added
        '''
        if self.index==None:
            dock=QDockWidget()
            self.docks.append(dock)
            dock.setWidget(widget)
            dock.setWindowTitle(name)
            return (True,dock)
        else:
            dock=self.docks[self.index]
            if self.index==len(self.docks)-1:
                self.index=None
            else:
                self.index+=1
            dock.setWidget(widget)
            dock.setWindowTitle(name)
            return (False,dock)
            
    def resetAll(self):
        '''
        Reset the window titles of All the QDockWidgets in self.docks and set self.index=0
        
        Returns:
            None
        '''
        if len(self.docks)==0:
            self.index=None
        else:
            for q in self.docks:
                q.setWindowTitle('')
                q.show()
            self.index=0
        
    def getEmpties(self):
        '''
        Return all the QDockWidgets which have no child in a list.
        
        Returns:
            list
        '''
        if self.index==None:
            answer=[]
        else:
            answer=self.docks[self.index:]
        return answer
        
class GraphContainer(QMainWindow):
    '''
    A container class which holds graphs
    '''
    DOCKOPTIONS=QMainWindow.AllowTabbedDocks|QMainWindow.AllowNestedDocks
    
    def __init__(self,que):
        super().__init__()
        self.setDockOptions(GraphContainer.DOCKOPTIONS)
        self.graphs={} #dict to manage graphs: {int: (Queue, GraphBase) }
        self.docks=DockList()
        self.que=que #the connection to the main process
        
        self.watchThread=watchQue(self.que,self)
        self.watchThread.addSignal.connect(self.addGraph)
        self.watchThread.dataSignal.connect(self.putData)
#        self.watchThread.removeSignal.connect(self.removeGraph)
        self.watchThread.resetSignal.connect(self.reset)
        self.watchThread.poisonSignal.connect(self.close)
        self.watchThread.start()
        
        #place the window to the right of the screen
        screen=QDesktopWidget().availableGeometry()
        height=screen.height()
        width=screen.width()/2
        self.setGeometry(width,40,width,height)
        
        #self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(kuchinawa.ICONPATH))
        self.setWindowTitle(kuchinawa.KUCHINAWA+' Graph Container')
        self.show()

    
    def addGraph(self,identifier,graph,name,args,kwargs):
        '''
        Embed 'graph' to QDockWidget and add it to self
        
        Paramters:
            identifier: int
                identifier to distinguish between graphs
            graph: class
                the class to generate
            args: tuple
                positional arguments to give to graph's __init__
            kwargs: dict
                keyword arguments to give to graph's __init__
        Returns:
            None
        '''
        g=graph(*args,**kwargs)
        mybool,dock=self.docks.setWidget(g,name)
        que=g.getQue()
        self.graphs[identifier]=(que,g)
        if mybool:
            self.addDockWidget(Qt.TopDockWidgetArea,dock)
        
    def putData(self,identifier,data):
        self.graphs[identifier][0].put(data) #self.graphs holds {int: (Queue, GraphBase)}
        
#    def removeGraph(self,identifier):
#        '''
#        Remove the graph identified by 'identifier'
#        
#        Parameters:
#            identifier: int
#                the key in self.graphs
#        Returns:
#            None
#        '''
#        mytuple=self.graphs[identifier]
#        que=mytuple[0]
#        graph=mytuple[1]
#        graph.setParent(None)
#        del(que)
#        del(graph)
        
    def reset(self):
        for mytuple in self.graphs.values(): #self.graphs holds {int: (Queue, GraphBase)}
            que=mytuple[0]
            graph=mytuple[1]
            graph.setParent(None)
            del(que)
            del(graph)
        self.docks.resetAll()
    
class GraphBase(pg.PlotWidget):
    '''
    A Base class which can be added to GraphContainer
    '''
    GRAPH_RATE=100  #update rate (/millisecond)
    
    def __init__(self):
        super().__init__()
        
        self.que=Queue()
        
        self.timer=QTimer()
        self.timer.timeout.connect(self.update)
        
        self.plt=self.plotItem
        self.plt.showGrid(x=True,y=True)
        fontCss = {'font-family': "Segoe UI, メイリオ", 'font-size': '14pt', "color": 'white'}
        self.plt.getAxis('bottom').setLabel(**fontCss)
        self.plt.getAxis('left').setLabel(**fontCss)
        
    def getQue(self):
        return self.que
        
    @abstractmethod
    def update(self):
        '''Implementation of graph update'''
        raise NotImplementedError('This method must be implemented in a subclass.')
        
    def start(self):
        self.timer.start(self.GRAPH_RATE)
        
class ScatterAll(GraphBase):
    '''
    Plot all data and highlight the latest point. Put a new data in a dict: {'x': x value,'y': y value}
    '''
    def __init__(self,xlabel,xunit,ylabel,yunit,color='w'):
        super().__init__()
        #Initialization of PlotItem
        self.xlabel=xlabel
        self.ylabel=ylabel
        
        self.x=[]
        self.y=[]

        self.point=None

        self.plt.setLabel('bottom',xlabel, units=xunit)
        self.plt.setLabel('left', ylabel, units=yunit)
        
        self.curve=self.plt.plot(self.x,self.y,pen=color)
        self.start()
        #set markers at latest values if data lenght is not zero.
        
    def update(self):
        mylist=self.empty_que()
        if len(mylist)>0:
            xappended=[d['x'] for d in mylist]
            self.x=self.x+xappended
            self.x_last=xappended[-1]
            yappended=[d['y'] for d in mylist]
            self.y=self.y+yappended
            self.y_last=yappended[-1]

            if not self.point==None:
                self.plt.removeItem(self.point)
                
            self.curve.setData(self.x,self.y)
            self.point=self.plt.plot([self.x_last],[self.y_last],symbolBrush='w')
        
    def empty_que(self):
        '''Take out data from the que and return them in a list.'''
        mylist=[]
        while True:
            if not self.que.empty():
                v=self.que.get()
                mylist.append(v)
            else:
                break
        return mylist
        
def initGraphContainer(que):
    app = QApplication(sys.argv)
    gc=GraphContainer(que)
    app.exec_()