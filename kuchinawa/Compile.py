# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 16:00:00 2017

@author: Yuki
"""

from PyQt5 import uic
import sys

def compileUi(path):
    '''
    Compile a .ui file made by QtDesigner to a .py file.
    
    Paramters:
        path: str
            the path to the .ui file
    Returns:
        str
            the path to the created .py file
    '''
    import re
    with open(path,'r') as i:
        result=re.match('.+\.ui',path)
        if result==None:
            raise Exception('Input file must be a file with the extension .ui')
        else:
            n_path=path.rstrip('.ui')+'.py'
            with open(n_path,'w') as o:
                 uic.compileUi(i,o)
    print('Compiled \''+path+'\' to \''+n_path+'\'')
   