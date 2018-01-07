# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 00:25:28 2017

@author: Yuki
"""

import logging
logger = logging.getLogger('Kuchinawa Log')
 
# ログレベルの設定
logger.setLevel(10)
 
# ログのファイル出力先を設定
fh = logging.FileHandler('kuchinawa.log')
logger.addHandler(fh)
 
# ログのコンソール出力の設定
sh = logging.StreamHandler()
logger.addHandler(sh)
 
# ログの出力形式の設定
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)