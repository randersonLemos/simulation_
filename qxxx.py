# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:58:55 2019

@author: randerson
"""


import subprocess
from settings import PUTTY_PATH


class Qxxx:
    @classmethod
    def _cmd_qstat_username(cls, username):
        command = str(PUTTY_PATH) +\
                " -load {} qstat -u {}".format(sett.Cluster.name, username)
        if verbose: print("qstat command:\n\t{}".format(command))
        return command


    @classmethod
    def _cmd_qstat_pid(cls, pid):
        command = (str(PUTTY_PATH) +\
                " -load {} qstat {}".format(sett.Cluster.name, pid)).strip()
        if verbose: print("qstat command:\n\t{}".format(command))
        return command


    @classmethod
    def _cmd_qstat_all(cls):
        command = str(PUTTY_PATH) +\
                " -load {} qstat".format(sett.Cluster.name)
        if verbose: print("qstat command:\n\t{}".format(command))
        return command


    @classmethod
    def qstat(cls, pid='', username='', verbose=False):
        if pid and username:
            raise Exception("Use of both arguments 'pid' and 'username' not allowed.")
        elif pid:
            process = subprocess.Popen(cls._cmd_qstat_pid(pid, verbose), shell=True)
        elif username:
            process = subprocess.Popen(cls._cmd_qstat_username(username, verbose), shell=True)
        else:
            process = subprocess.Popen(cls._cmd_qstat_all(verbose), shell=True)

        stdout, stderr = process.communicate()
        if stdout: print(stdout.decode('utf-8'))
        else: raise ProcessLookupError
