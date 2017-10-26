# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 11:33:04 2017

@author: Jackson
"""
import sys
import pandas as pd

class File():
    '''
    Implements a csv type file instance.
    '''
    
    def __init__(self,path,sep='\t',comment='#'):
        super().__init__()
        self.path=path
        self.file=open(path,'a+')
        self.sep=sep
        self.comment=comment
        self._before_writing=True
        
    def close(self):
        self.file.close()
        
    def write_comment(self,string):
        '''
        Add a comment to the head of the file
        
        Parameters
            string: string
                A string to be added. \n is not needed.
                
        Returns
            None
        '''
        if self._before_writing:
            self.file.write(self.comment+string+'\n')
        else:
            raise Exception('Comments must be written before starting to write data')
    
    def write_header(self,mylist):
        '''
        Set headers to the file.
        
        Parameters
            mylist: list
                The header names.
                
        Returns
            None
        '''
        if self._before_writing:
            self.columns=pd.DataFrame(columns=mylist)
            self.columns.to_csv(self.file,sep=self.sep,index=False)
            self._before_writing=False
        else:
            raise Exception('Headers are already written')
    
    def write_data(self,mydict):
        '''
        Write data to the file
        
        Parameters
            mydict: dictionary
                The keys corresponds to the headers.
                
        Returns
            None
        '''
        if self._before_writing:
            raise Exception('Headers has not been set yet.')
        else:
            row=self.columns.append(mydict,ignore_index=True)
            row.to_csv(self.file,sep=self.sep,index=False,header=False)