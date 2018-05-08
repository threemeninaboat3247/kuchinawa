# -*- coding: utf-8 -*-

""" --- Description ---
    Module:
        Logger.py
    Abstract:
        A module for logging
    Modified:
        threemeninaboat3247 2018/04/30
    ---    End      ---
"""
# Standard library imports
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