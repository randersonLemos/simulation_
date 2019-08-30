# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:04:54 2019

@author: randerson
"""

import utils
import settings as sett
    
def well_generator(sim_folder):
    from well2.scripts.utils import gen_prod_icv as gpi
    from well2.scripts.utils import gen_inje_wag as giw
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
        , ip.icv_start
        , ip.icv_control
        , sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / 'wells'
        )

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
    idx = 1    
    sim_folder = 'sim_{:03d}'.format(idx)
    
    utils.setting_files(sim_folder)
    well_generator(sim_folder)
    sim = utils.run_imex_remote(sim_folder, True, True)
    
    while sim.is_alive(): pass

    utils.generate_report(sim_folder, True)