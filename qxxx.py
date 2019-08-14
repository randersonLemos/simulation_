# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:58:55 2019

@author: randerson
"""

import subprocess
import settings as sett


class Qxxx:     
    stdout = ''
    stderr = ''
    @classmethod
    def qstat(cls, verbose=False):
        command = str(sett.Paths.putty) +\
        " -load {} qstat".format(sett.Cluster.name)
        if verbose: print('qtat command:\n\t{}'.format(command))
        process = subprocess.Popen(command, shell=True)
        stdout, stderr = process.communicate()
        if stdout and stderr:
            cls.stdout = stdout.decode('utf-8')
            cls.stderr = stderr.decode('utf-8')
        else:
            raise ProcessLookupError