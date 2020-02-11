# -*- coding: utf-8 -*-
"""
File for generation of wells and simulation running.
Codes for fire simulation are commented.
"""


def producers(sim_folder):
    from config import settings as sett
    from assembly.scripts.producer_dual_icv import producer_dual_icv
    from inputt.loader import prod_lst
    for prod in prod_lst:
        prod.load_more_more()
        producer_dual_icv(  prod.name
                          , prod.group
                          , prod.operate
                          , prod.monitor
                          , prod.geometry
                          , prod.perf_ff
                          , prod.perf_table
                          , prod.time_open
                          , prod.time_on
                          , prod.layerclump
                          , []#prod.icv_operation
                          , []#prod.icv_control_law
                          , sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder / 'wells'
                          )


def injectors_wag(sim_folder):
    from config import settings as sett
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
    import pathlib
    from scripts import utils

    sim_folder_group = pathlib.Path('DEFAULT')
    #sim_folder_group = pathlib.Path('REFERENCE')
    sim_folder = sim_folder_group / 'sim_001'

    utils.set_folders(sim_folder)

    producers(sim_folder)
    injectors_wag(sim_folder)

    #sim = utils.run_imex_remote(sim_folder, True, True)
    #while sim.is_alive(): pass
    #import time; time.sleep(5)    
    #utils.run_report(sim_folder, True)