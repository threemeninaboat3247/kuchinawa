# -*- coding: utf-8 -*-
"""
Created on Mon May 15 21:26:18 2017

@author: Press150
"""

import visa
import re

class GpibInst():
    pattern=re.compile(r'^[\+-]?\d*\.?\d*E[\+-]?\d*')
    def __init__(self,gpib):
        rm=visa.ResourceManager()
        self.inst = rm.get_instrument("GPIB::"+ str(int(gpib)))
        
    def query(self,command,raw_string=False):
        answer=self.inst.query(command)
        if raw_string:
            return answer
        else:
            body=self.pattern.match(answer).group()
            return float(body)
    
    def write(self,command):
        self.inst.write(command)
        return True