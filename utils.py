# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 16:06:02 2019

@author: randerson
"""

import settings as sett
from pathlib import Path

def setting_files(sim_folder):
    folder_origin = sett.LOCAL_ROOT / 'dat2' 
    folder_destiny = Path(sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder)
    
    from distutils.file_util import copy_file
    from distutils.dir_util import copy_tree   
    
    folder_origin = Path(folder_origin)
    folder_destiny = Path(folder_destiny)
    
    (folder_destiny).mkdir(parents=True, exist_ok=True)
    (folder_destiny / 'includes').mkdir(parents=True, exist_ok=True)
    
    copy_file(str(folder_origin / sett.DAT_NAME), str(folder_destiny))
    copy_file(str(folder_origin / sett.RWD_NAME), str(folder_destiny))
    copy_tree(str(folder_origin / 'includes'), str(folder_destiny / 'includes'))
    
def run_imex_local(sim_folder, see_log, verbose):
    from run2.scripts import imex

    imex.Imex_Local.set_exe_imex(sett.LOCAL_IMEX_EXE)    
    
    imexx = imex.Imex_Local(
              exe = sett.LOCAL_IMEX_EXE
            , path_to_dat = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.DAT_NAME 
            , folder_to_output = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder
            , see_log = see_log
            , verbose = verbose
            )
    imexx.run()
    return imexx

def run_imex_remote(sim_folder, see_log, verbose):
    from run2.scripts import imex
    
    imex.Imex_Remote.set_exe_imex(sett.REMOTE_IMEX_EXE)    
    imex.Imex_Remote.set_exe_putt(sett.LOCAL_PUTT_EXE)
    imex.Imex_Remote.set_local_root(sett.LOCAL_ROOT)
    imex.Imex_Remote.set_user(sett.USER)
    imex.Imex_Remote.set_cluster_name(sett.CLUSTER_NAME)
    
    imexx = imex.Imex_Remote(
              path_to_dat = sett.REMOTE_ROOT / sett.RES_FOLD / sim_folder / sett.DAT_NAME 
            , folder_to_output = sett.REMOTE_ROOT / sett.RES_FOLD / sim_folder                        
            , queue_kind = sett.QUEUE_KIND
            , nr_processors = sett.NR_PROCESSORS            
            , see_log = see_log
            , verbose = verbose
            )
    imexx.run()
    return imexx

def generate_report(sim_folder, verbose):
    from run2.scripts import report

    report.Report.set_exe(sett.LOCAL_REPO_EXE)
    
    repo = report.Report(
              path_to_rep = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.REP_NAME 
            , path_to_rwd = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.RWD_NAME 
            , path_to_irf = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.IRF_NAME 
            , folder_to_output = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder
            , verbose= verbose
            )
    repo.run()    