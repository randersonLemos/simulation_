# -*- coding: utf-8 -*-
"""
File for generation of wells and simulation running.
Codes for fire simulation are commented.
"""


def producers(sim_folder, prod):
    from config import settings as sett
    from assembly.scripts.producer_dual_icv import producer_dual_icv
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
    import numpy
    import pathlib
    from scripts import utils
    from dictionary.scripts.keywords import Keywords as kw
 
    qtys = [(kw.gor(),  val) for val in numpy.linspace(250, 5000, 20)]

    sim_folder_group = pathlib.Path('DEFAULT')
    #sim_folder_group = pathlib.Path('WELL')
    sims = []
    for idx, qty in enumerate(qtys):
        sim_folder = sim_folder_group / 'sim_{:03d}'.format(idx+1)
        
        utils.set_folders(sim_folder)
        
        from inputt.loader import prod_lst
        for prod in prod_lst:
            prod = prod.load_more_more()
            prod.monitor.append([qty[0], qty[1], kw.shutin()])
            producers(sim_folder, prod)            

        injectors_wag(sim_folder)        
        sims.append((sim_folder, utils.run_imex_remote(sim_folder, False, True)))
    while sims:
        for idx, (sim_folder, sim) in enumerate(sims):
            if sim.is_alive():
                pass
            else:
                import time; time.sleep(5)    
                utils.run_report(sim_folder, True)
                del sims[idx]
                break