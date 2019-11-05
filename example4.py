# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:04:54 2019

@author: randerson
"""


def producers_icv_binary(sim_folder, well):
    from config.scripts import settings as sett
    from assembly.scripts.producer_dual_icv import producer_dual_icv
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
                      , well.icv_start
                      , well.icv_operational
                      , sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder / 'wells'
                      )


def injectors_wag(sim_folder):
    from config.scripts import settings as sett
    from assembly.scripts.injector_dual_wag import injector_dual_wag
    from inputt.scripts.infos import injes_lst

    for name in injes_lst:
        try: well = __import__('inputt.scripts.{}'.format(name), fromlist=name)
        except ImportError: raise('Error importing', 'inputt.scripts.{}'.format(name), '.')
        injector_dual_wag(   name
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


if __name__ == '__main__':
    from scripts import utils
    from config.scripts import settings as sett
    from dictionary.scripts.dictionary import Keywords as kw

    sim_folder = 'sim_001'
    path_to_sim_folder = sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder

    utils.set_folders(sim_folder)

    from valve.scripts import icv
    from inputt.scripts.infos import prods_lst
    for name in prods_lst:
        try: well = __import__('inputt.scripts.{}'.format(name), fromlist=name)
        except ImportError: raise('Error importing', 'inputt.scripts.{}'.format(name), '.')
        icvv = icv.ICV(well.icv_nr)
        well.icv_operational = icvv.incremental(
                          (  (kw.gor()  , 0.0, 500.0, 750.0, 1000.0,)
                           , (kw.wcut() , 0.0, 0.85, 0.90, 0.95,)
                           ,
                           )
                        , (1.0, 0.50, 0.0,)
                        , ('OR',)
                        )
        icvv.write(path_to_sim_folder / sett.IRF_NAME)
        producers_icv_binary(sim_folder, well)

    injectors_wag(sim_folder)

    sim = utils.run_imex_remote(sim_folder, True, True)

    while sim.is_alive(): pass

    utils.run_report(sim_folder, True)