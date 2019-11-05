# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:04:54 2019

@author: randerson
"""


def producers(sim_folder):
    from config.scripts import settings as sett
    from assembly.scripts.producer_dual_icv import producer_dual_icv
    from inputt.scripts.infos import prods_lst

    for name in prods_lst:
        try: well = __import__('inputt.scripts.{}'.format(name), fromlist=name)
        except ImportError: raise('Error importing', 'inputt.scripts.{}'.format(name), '.')
        producer_dual_icv(  name
                          , well.group
                          , well.operate
                          , well.monitor
                          , well.geometry
                          , well.perf
                          , well.completion
                          , well.openn
                          , well.on_time
                          , well.layerclump
                          , []
                          , []
                          , sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder / 'wells'
                          )


def injectors_wag(sim_folder):
    from config.scripts import settings as sett
    from assembly.scripts.injector_dual_wag import injector_dual_wag
    from inputt.scripts.infos import injes_lst

    for name in injes_lst:
        try: well = __import__('inputt.scripts.{}'.format(name), fromlist=name)
        except ImportError: raise('Error importing', 'inputt.scripts.{}'.format(name), '.')
        injector_dual_wag(  name
                          , well.group
                          , well.operate
                          , well.monitor
                          , well.geometry
                          , well.perf
                          , well.completion
                          , well.openn
                          , well.on_time
                          , well.wag_cycle
                          , well.layerclump
                          , sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder / 'wells'
                          )


from scripts import utils


if __name__ == '__main__':
    sim_folder = 'sim_001'

    utils.set_folders(sim_folder)

    producers(sim_folder)
    injectors(sim_folder)

    sim = utils.run_imex_remote(sim_folder, True, True)

    while sim.is_alive(): pass

    utils.run_report(sim_folder, True)