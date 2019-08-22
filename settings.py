# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:04:54 2019
@author: randerson
"""
from pathlib import Path

N_SIMS = 1

MACHINE = 'remote'
#MACHINE = 'local'
if MACHINE == 'local':    
    ROOT_LOCAL = Path('U:/simulation')
    IMEX_EXE = Path('C:/"Program Files (x86)"/CMG/IMEX/2017.10/Win_x64/EXE/mx201710.exe')
    MAIN_FOLDER = 'sims'    
    USER = ''
    QUEUE_KIND = ''
    CLUSTER_NAME = ''
if MACHINE == 'remote':
    ROOT_LOCAL = Path('U:/simulation')
    ROOT_REMOTE = Path('/home/randerson/simulation')
    IMEX_EXE = Path('/mnt/simuladores/CMG/imex/2017.10/linux_x64/exe/mx201710.exe')
    MAIN_FOLDER =  'sims'    
    USER = 'randerson'
    CLUSTER_NAME = 'hpc02'
    QUEUE_KIND = 'longas'
    PUTTY_EXE = Path('C:/\"Program Files (x86)"/PuTTY/plink.exe')

REPORT_EXE = Path('C:/\"Program Files (x86)"/CMG/BR/2017.10/Win_x64/EXE/report.exe')
