# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:04:54 2019

@author: randerson
"""


def producers_icv_binary(sim_folder, well):
    from config.scripts import settings as sett
    from assembly.scripts.producer_dual_icv import producer_dual_icv
    producer_dual_icv(  well.name
                      , well.group
                      , well.operate
                      , well.monitor
                      , well.geometry
                      , well.perf_ff
                      , well.perf_table
                      , well.time_open
                      , well.time_on
                      , well.layerclump
                      , well.icv_operation
                      , well.icv_control_law
                      , sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder / 'wells'
                      )


def injectors_wag(sim_folder):
    from config.scripts import settings as sett
    from assembly.scripts.injector_dual_wag import injector_dual_wag
    from inputt.loader import inje_lst
    for inje in inje_lst:
        inje.load_more_more()
        injector_dual_wag(  inje.name
                          , inje.group
                          , inje.operate
                          , inje.monitor
                          , inje.geometry
                          , inje.perf_ff
                          , inje.perf_table
                          , inje.time_open
                          , inje.time_on
                          , inje.wag_operation
                          , inje.layerclump
                          , sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder / 'wells'
                          )


if __name__ == '__main__':
    from scripts import utils
    from config.scripts import settings as sett
    from dictionary.scripts.keywords import Keywords as kw

    sim_folder = 'sim_001'
    path_to_sim_folder = sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder

    utils.set_folders(sim_folder)

    from valve.scripts import icv
    from inputt.loader import prod_lst
    for prod in prod_lst:
        prod.load_more_more()
        icvv = icv.ICV(prod.icv_nr)
        prod.icv_operation = (2008, 183, 200)
        prod.icv_control_law = icvv.binary([kw.gor(), kw.greater_than(), 1000.0, 'OR', '*STO-RP', kw.less_than(), 250],[kw.wcut(), kw.greater_than(), 95.0])
        icvv.write(path_to_sim_folder / sett.INF_NAME)
        producers_icv_binary(sim_folder, prod)

    injectors_wag(sim_folder)

    sim = utils.run_imex_remote(sim_folder, True, True)
    #while sim.is_alive(): pass
    #utils.run_report(sim_folder, True)