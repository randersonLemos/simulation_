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
    import numpy
    import itertools
    from scripts import utils
    from config.scripts import settings as sett
    from dictionary.scripts.dictionary import Keywords as kw
    
    import random
    from inputt.scripts.infos import prods_lst

    bag = [123, 153, 183, 213, 243]
    freqs = []
    nr_sims = 1000
    for i in range(nr_sims):
        dic = {}
        for well in prods_lst:
            dic[well] = random.choice(bag)
        freqs.append(dic)
    
    sims = []
    for idx, freq in enumerate(freqs):
        sim_folder = 'SIM_ICV_2_STGS_FREQ/sim_{:03d}'.format(idx+1)
        path_to_sim_folder = sett.LOCAL_ROOT / sett.SIMS_FOLDER / sim_folder

        utils.set_folders(sim_folder)

        from valve.scripts import icv
        for name in prods_lst:
            try: well = __import__('inputt.scripts.{}'.format(name), fromlist=name)
            except ImportError: raise('Error importing', 'inputt.scripts.{}'.format(name), '.')
            icvv = icv.ICV(well.icv_nr)
            well.icv_operational = icvv.binary(('*GOR', '>', 1000.0))
            well.icv_start = (2008, freq[name], 500)
            if well == 'Wildcat':
                well.icv_start = []
            
            icvv.write(path_to_sim_folder / sett.INF_NAME)
            with open(path_to_sim_folder / sett.INF_NAME, 'a') as fh:
                fh.write(freq.__repr__())
            
            producers_icv_binary(sim_folder, well)

        injectors_wag(sim_folder)

        sims.append((sim_folder, utils.run_imex_remote(sim_folder, False, True)))

    while sims:
        for idx, (_,sim) in enumerate(sims):
            if sim.is_alive():
                pass
            else:
                del sims[idx]
                break

    for (sim_folder,_) in sims:
        utils.run_report(sim_folder, True)