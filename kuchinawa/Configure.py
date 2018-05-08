# -*- coding: utf-8 -*-

""" --- Description ---
    Module:
        Configure.py
    Abstract:
        A module for configure file.
    Modified:
        threemeninaboat3247 2018/04/30
    ---    End      ---
"""
# Standard library imports
import os,copy,pickle

# Local imports
import kuchinawa
from kuchinawa import Logger

class Configure:
    _CONFIG_PATH=os.path.join(kuchinawa.ENTRYPOINT,'config.dump')
    _DEFAULT_CONFIG={'config_graph_clear':True,'config_graph_rate':100}
    _config=copy.copy(_DEFAULT_CONFIG)
    
    @classmethod
    def loadConfigure(cls,path=_CONFIG_PATH):
        '''
        Load the configure file
        
        Parameters:
            path: str
                the path to the configure file
        '''
        try:
            with open(path,'rb') as config:
                cls._config=pickle.load(config)
                Logger.logger.debug('Loaded the configure file from {}'.format(path))
        except:
            Logger.logger.debug('Failed loading the configure file from {}'.format(path))
    
    @classmethod
    def saveConfigure(cls,path=_CONFIG_PATH):
        '''
        Save the configure to the file
        
        Parameters:
            path: str
                the path to the configure file
        '''
        with open(path,'wb') as config:
            pickle.dump(cls._config,config)
            Logger.logger.debug('Saved the configure file to {}'.format(path))
    
    @classmethod
    def resetConfigure(cls):
        '''
        Reset the configure
        '''
        cls._config=copy.copy(cls._DEFAULT_CONFIG)
        Logger.logger.debug('Reset the configure')
        
    @classmethod
    def getConfigure(cls):
        '''
        Get the configure
        
        Returns:
            dict
                the current configure
        '''
        return copy.copy(cls._config)
    
    @classmethod
    def setEachConfigure(cls,key,value):
        '''
        Set each of the configure
        
        Parameters:
            key: str
                the key of the configure to change
            value: object
                the value of the configure to be set
        '''
        cls._config[key]=value
    
    @classmethod
    def setAllConfigure(cls,mydict):
        '''
        Set all the configure at once
        
        Parameters:
            mydict: dict
                the configure to be set
        '''
        cls._config=copy.copy(mydict)
    