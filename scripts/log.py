# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 15:05:49 2019

@author: randerson
"""

import subprocess
from config.scripts import settings as sett

class Log:
    @staticmethod
    def see(sim_folder, size_tail=15, verbose=True):
        command = 'powershell Get-Content {} -tail {}'\
            .format(sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder / 'main.log', size_tail)
        if verbose: print('command see:\n\t{}'.format(command))
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, _ = process.communicate()        
        print(stdout.decode('utf-8'))        