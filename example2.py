# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 07:57:00 2019

@author: randerson
"""

from scripts import utils
import settings as sett      

def prod_generator(sim_folder, icv_start, icv_control):
    from _well2.scripts.utils import gen_prod_icv as gpi
    from _well2.scripts.misc import Keywords as kw

    from _well2.scripts import info_producers as ip

    cont_repeat = '{} {}'.format(kw.cont(), kw.repeat())

    operate = [ (kw.max(), kw.stl(), 3000.0, cont_repeat)
               ,(kw.min(), kw.bhp(),  295.0, cont_repeat)
              ]
    monitor = [(kw.wcut(), 0.95, kw.shutin())]
    gpi(  operate
        , monitor
        , ip.well_completion
        , ip.well_opening
        , ip.well_on_time
        , ip.icv_layerclump
        , icv_start
        , icv_control
        , sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / 'wells'
        )

def inje_generator(sim_folder):
    from _well2.scripts.utils import gen_inje_wag as giw
    from _well2.scripts.misc import Keywords as kw
    
    from _well2.scripts import info_injectors as ii
    
    cont_repeat = '{} {}'.format(kw.cont(), kw.repeat())
    
    operate = [ ('G', kw.max(), kw.stg(), 3000000.0, cont_repeat)
               ,('G', kw.max(), kw.bhp(),     540.0, cont_repeat)
               ,('W', kw.max(), kw.stw(),    5000.0, cont_repeat)
               ,('W', kw.max(), kw.bhp(),     470.0, cont_repeat)
              ]
    monitor = []
    giw(  operate
        , monitor
        , ii.well_completion
        , ii.well_opening
        , ii.well_on_time
        , ii.well_wag
        , sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / 'wells'
        )            
   
    
if __name__ == '__main__':     
    import numpy
    import itertools
    from scripts import icvs

    GORS  = numpy.linspace(1000, 10000, 10)
    WCUTS = numpy.linspace(70.0, 96.0, 5)
    lst   = list(itertools.product(GORS, WCUTS))

    sims = []
    sim_folders = []
    for idx, (GOR, WCUT) in enumerate(lst):
        sim_folder = 'sim_{:03d}'.format(idx+1)
        sim_folders.append(sim_folder)
    
        utils.setting_files(sim_folder)
        
        #prod_generator(sim_folder, icv_start=[], icv_control=[])

        #icv_control = icvs.icv_control_incremental(GOR, WCUT, 2.0, 1.2, 5)        
        #utils.write_control_strategy(sim_folder, list(icv_control.values())[0])
        #prod_generator(sim_folder, icv_start=icvs.icv_start(), icv_control=icv_control)
        
        inje_generator(sim_folder)
        sims.append(utils.run_imex_remote(sim_folder, see_log=False, verbose=True))      
    
    while sims:
        for idx, sim in enumerate(sims):
            if sim.is_alive():
                pass
            else:
                del sims[idx]
                break
            
    for sim_folder in sim_folders:        
        utils.generate_report(sim_folder, True)