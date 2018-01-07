# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 12:36:24 2017

@author: Yuki
"""

'''
The widgets for the configure of Kuchinawa in the setting window 
made by QtDesigner have names starting with 'config_'.
'''

from kuchinawa import Setting,Configure
from PyQt5.QtWidgets import QComboBox,QSpinBox
from distutils.util import strtobool

class Configure_interface():
    PREFIX='config_'
    
    def __init__(self,mydict):
        '''
        Make the interface to interact with the configure window
        
        Parameters:
            mydict: dict
                dictionary whose key and value are widget name and widget respectively
        '''
        self.configures={}
        for key,widget in mydict.items():
            if key.startswith(Configure_interface.PREFIX):
                self.configures[key]=widget
    
    def set_value(self,key,value):
        '''
        Set value to a widget
        
        Parameters:
            key: str
                the widget's name
            value: bool,int,float,etc.
                the value to be set
        '''
        widget=self.configures[key]
        if isinstance(widget,QComboBox):#index 0: True, index1: False
            if value:
                widget.setCurrentIndex(0)
            else:
                widget.setCurrentIndex(1)
        elif isinstance(widget,QSpinBox):
            widget.setValue(value)
            
    def get_value(self,key):
        '''
        Return the value of a widget
        
        Parameters:
            key: str
                the widget's name
        Returns:
            bool,int,float,etc.
        '''
        widget=self.configures[key]
        if isinstance(widget,QComboBox):#index 0: True, index1: False
            return bool(strtobool(widget.currentText()))
        elif isinstance(widget,QSpinBox):
            return widget.value()
        
    def set_all_values(self,mydict):
        '''
        Set all the values to the widgets at once
        
        Parameters:
            mydict: dict
                dictionary whose key and value are widget name and widget respectively
        '''
        for key,value in mydict.items():
            self.set_value(key,value)
            
    def get_all_values(self):
        '''
        Get all the values from the widgets at once
        
        Returns:
            dict
        '''
        answer={}
        for key in self.configures.keys():
            answer[key]=self.get_value(key)
        return answer
                

class My_Ui_Form(Setting.Ui_Form):
    def make_interface(self):
        self._interface=Configure_interface(vars(self))
        self.pushButton_ok.pressed.connect(self.ok_pressed)
        self.pushButton_cancel.pressed.connect(self.cancel_pressed)
        
    def ok_pressed(self):
        window_config=self._interface.get_all_values()
        Configure.Configure.setAllConfigure(window_config)
        
    def cancel_pressed(self):
        current=Configure.Configure.getConfigure()
        self._interface.set_all_values(current)
        