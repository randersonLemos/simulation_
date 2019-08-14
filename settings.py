# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:04:54 2019
@author: randerson
"""


from pathlib import Path, PurePosixPath


MACHINE = 'remote'
#MACHINE = 'local'
if MACHINE == 'local':
    ROOT = Path('U:/simulation')
    IMEX_EXE = Path('C:/"Program Files (x86)"/CMG/IMEX/2017.10/Win_x64/EXE/mx201710.exe')
    IMEX_FOLDER_DAT = 'results'
    IMEX_FOLDER_OUT = 'results'
    USER = ''
    QUEUE_KIND = ''
    CLUSTER_NAME = ''
elif MACHINE == 'remote':
    ROOT = PurePosixPath('/home/randerson/simulation')
    ROOT_LOCAL = Path('U:/simulation')
    IMEX_EXE = PurePosixPath('/mnt/simuladores/CMG/imex/2017.10/linux_x64/exe/mx201710.exe')
    IMEX_FOLDER_DAT =  'results'
    IMEX_FOLDER_OUT =  'results'
    USER = 'randerson'
    CLUSTER_NAME = 'hpc02'
    QUEUE_KIND = 'longas'
else:
    raise ValueError("MACHINE must be 'local' or 'remote'")


#REPORT_EXE = 'C:\\Program Files (x86)\\CMG\\BR\\2017.10\\Win_x64\\EXE\\report.exe'
#REPORT_IRF = 'U:/simulation/results/main.irf'
#REPORT_FOLDER_OUT =  'U:/simulation/results'


PRODS_KEYS       = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
PRODS_NAMES      = {1:'PRK014', 2:'PRK028', 3:'PRK045', 4:'PRK052', 5:'PRK060', 6:'PRK061', 7:'PRK083', 8:'PRK084', 9:'PRK085', 10:'Pwildc'}
PRODS_OPEN_TIMES = {1:'1704.0', 2:'1612.0', 3:'1369.0', 4:'1765.0', 5:'1492.0', 6:'1673.0', 7:'1431.0', 8:'1308.0', 9:'1247.0', 10:'1553.0'}
PRODS_ICVS_QTYS  = {1:3       , 2:2       , 3:3       , 4:2       , 5:2       , 6:3       , 7: 3      , 8:2       , 9:3       , 10:0       }

INJES_KEYS = [1, 2, 3, 4, 5, 6, 7, 8]
INJES_NAMES = {1:'IRK004', 2:'IRK028', 3:'IRK029', 4:'IRK036', 5:'IRK049', 6:'IRK050', 7:'IRK056', 8:'IRK063'}
INJES_OPEN_TIMES = {1:['WATER','1734.0'], 2:['WATER','1643.0'], 3:['WATER','1400.0'], 4:['GAS','1584.0'], 5:['GAS','1522.0'], 6:['WATER','1461.0'], 7:['GAS','1339.0'], 8:['GAS','1278.0']}
INJES_WAGSS = {1:'GAS', 2:'GAS', 3:'GAS', 4:'WATER', 5:'WATER', 6:'GAS', 7:'WATER', 8:'WATER'}


class Paths:
    putty = Path('C:/\"Program Files (x86)"/PuTTY/plink.exe')    
    
class Cluster:
    name = 'hpc02'