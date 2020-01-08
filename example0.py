# -*- coding: utf-8 -*-
"""
File for generation of wells and simulation running.
Codes for fire simulation are commented.
"""


def producers(path_to_save):
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
                          , path_to_save
                          )


def injectors_wag(path_to_save):
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
                          , path_to_save
                          )


from config.scripts import settings as sett


if __name__ == '__main__':
    path_to_save = sett.LOCAL_ROOT / sett.SIMS_FOLDER / 'wells'
    producers(path_to_save)
    injectors_wag(path_to_save)