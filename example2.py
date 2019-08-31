# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:04:54 2019

@author: randerson
"""

import utils
import settings as sett      

def prod_generator(sim_folder, icv_start, icv_control):
    from well2.scripts.utils import gen_prod_icv as gpi
    from well2.scripts.misc import Keywords as kw

    from well2.scripts import info_producers as ip

    operate = [ (kw.max(), kw.stl(), 3000.0, kw.cont_repeat())
               ,(kw.min(), kw.bhp(),  295.0, kw.cont_repeat())
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
    from well2.scripts.utils import gen_inje_wag as giw
    from well2.scripts.misc import Keywords as kw
    
    from well2.scripts import info_injectors as ii
    
    operate = [ ('G', kw.max(), kw.stg(), 3000000.0, kw.cont_repeat())
               ,('G', kw.max(), kw.bhp(),     540.0, kw.cont_repeat())
               ,('W', kw.max(), kw.stw(),    5000.0, kw.cont_repeat())
               ,('W', kw.max(), kw.bhp(),     470.0, kw.cont_repeat())
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
    
    GORS  = numpy.linspace(3000, 30000, 10)
    WCUTS = numpy.linspace(0.7, 0.95, 6)
    lst   = list(itertools.product(GORS, WCUTS))
    
    for idx, (GOR, WCUT) in enumerate(lst):
        sim_folder = 'sim_icv_control_{:03d}'.format(idx+1)
    
        utils.setting_files(sim_folder)
        prod_generator(sim_folder, icv_start=utils.icv_start(), icv_control=utils.icv_control_close(GOR, WCUT))
        inje_generator(sim_folder)
    
        sims = []
        sims.append(utils.run_imex_remote(sim_folder, see_log=False, verbose=True))
        
    csim = itertools.cycle(sims)
    for sim in csim:
        sim.is_alive()