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
    import numpy
    import pathlib
    import itertools
    from scripts import utils
    from config.scripts import settings as sett
    from dictionary.scripts.keywords import Keywords as kw

    qtys = [(kw.gor(),  val) for val in numpy.linspace(250, 5000, 20)]

    #sim_folder_group = pathlib.Path('DEFAULT')
    sim_folder_group = pathlib.Path('SIM_ICV_04_STG')
    sims = []
    for idx, qty in enumerate(qtys):
        sim_folder = sim_folder_group / 'sim_{:03d}'.format(idx+1)

        utils.set_folders(sim_folder)

        from valve.scripts import icv
        from inputt.loader import prod_lst
        for prod in prod_lst:
            prod.load_more_more()
            icvv = icv.ICV(prod.icv_nr)
            minn = 0.50*qty[1]
            maxx = qty[1]
            inte = (maxx-minn) / 3
            icvv.add_rule([qty[0], kw.greater_than(),  minn         , 0.75])
            icvv.add_rule([qty[0], kw.greater_than(),  minn +   inte, 0.50])
            icvv.add_rule([qty[0], kw.greater_than(),  minn + 2*inte, 0.25])
            icvv.add_rule([qty[0], kw.greater_than(),  minn + 3*inte, 0.00])
            icvv.write(sim_folder)
            prod.icv_operation = (2008, 183, 200)
            prod.icv_control_law = icvv.get_control_law()
            producers_icv_binary(sim_folder, prod)

        injectors_wag(sim_folder)

   #     sims.append((sim_folder, utils.run_imex_remote(sim_folder, False, True)))

   # while sims:
   #     for idx, (sim_folder ,sim) in enumerate(sims):
   #         if sim.is_alive():
   #             pass
   #         else:
   #             utils.run_report(sim_folder, True)
   #             del sims[idx]
   #