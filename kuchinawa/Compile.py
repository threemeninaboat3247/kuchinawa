# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 16:00:00 2017

@author: Yuki
"""

from PyQt5 import uic
import sys,os,shutil
import kuchinawa.Template

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
    def checkLines(target,lines):
        for index,line in enumerate(lines):
            if target in line:
                return index
    
    other,ext=os.path.splitext(path)
    if not ext=='.ui':
        raise Exception('Input file must be a file with the extension .ui')
    else:
        with open(path,'r') as i:
            o_path=other+'_ui.py'
            with open(o_path,'w') as o:
                uic.compileUi(i,o)
                print('{:*^50}'.format('compiled'))
                print('Source: {0}'.format(path))
                print('Output: {0}'.format(o_path))
        pro_path=other+'.py'
        if os.path.isfile(pro_path):
            pass
        else:
            #create a template file
            temp_path=kuchinawa.Template.__file__
            with open(temp_path,'r') as temp:
                lines=temp.readlines()
            
            index=checkLines('class Sample(Main):',lines)
            directory,module=os.path.split(other)
            module_name=module+'_ui'
            import_str='import '+module_name+'\n\n'
            lines.insert(index,import_str)
            
            index=checkLines('super().__init__()',lines)
            super_str=lines[index]
            indent=super_str.split('super()')[0]
            instantiate_str=indent+'self.ui='+module_name+'.Ui_Form()\n'
            set_str=indent+'self.setUI(self.ui)\n'
            lines.insert(index+1,instantiate_str)
            lines.insert(index+2,set_str)
            
            with open(pro_path,'w') as program:
                program.writelines(lines)
                print('{:*^50}'.format('generated a template file'))
                print('Template: {0}'.format(pro_path))