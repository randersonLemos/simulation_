# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 15:05:49 2019

@author: randerson
"""


import subprocess
import settings as sett


root = sett.ROOT_LOCAL
if sett.MACHINE == 'remote': root = sett.ROOT_REMOTE


class Log:
    @classmethod
    def see(cls, nr_sim, size_tail=15, verbose=True):
        command = 'powershell Get-Content {} -tail {}'\
            .format(str(sett.ROOT_LOCAL / sett.MAIN_FOLDER / 'sim_{:03d}'.format(nr_sim) / 'main.log'), size_tail)
        if verbose: print('command see:\n\t{}'.format(command))
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, _ = process.communicate()        
        print(stdout.decode('utf-8'))        