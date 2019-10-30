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
   
def write_icv_infos(sim_folder, GOR, WCUT, fac_GOR, fac_WCUT, nr_stages):
    path_to_inf = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.INF_NAME 
    with path_to_inf.open('w') as fh:
        fh.write('### Multiposition ICVs ###\n')
        fh.write('nr. stages: {}\n'.format(nr_stages))
        fh.write('ref. GOR: {}\n'.format(GOR))
        fh.write('fac. GOR: {}\n'.format(fac_GOR))
        fh.write('ref. WCUT: {}\n'.format(WCUT))
        fh.write('fac. WCUT: {}\n'.format(fac_WCUT))
    
if __name__ == '__main__':     
    import numpy
    import itertools
    from scripts import icvs

    GORS  = numpy.linspace(250, 2500, 19)
    WCUTS = numpy.linspace(75.0, 95.0, 5)
    lst   = list(itertools.product(GORS, WCUTS))

    Icv_settings = [
            (1.5,1.2,5) ,(2.0,1.2,5) ,(3.0,1.2,5)            
           ,(1.5,1.2,10),(2.0,1.2,10),(3.0,1.2,10)
           ,(1.5,1.2,15),(2.0,1.2,15),(3.0,1.2,15)
           ]

    sims = []
    sim_folders = []    
    for icv_settings in Icv_settings:

        for idx, (GOR, WCUT) in enumerate(lst):
            sim_folder = 'sim_{}{}{}_{:03d}'.format(int(10*icv_settings[0]), int(10*icv_settings[1]), int(10*icv_settings[2]), idx+1)
            sim_folders.append(sim_folder)
        
            #utils.setting_files(sim_folder)
            
            #prod_generator(sim_folder, icv_start=[], icv_control=[])
    
            #icv_control = icvs.icv_control_incremental(GOR, WCUT, icv_settings[0], icv_settings[1], icv_settings[2])        
            write_icv_infos(sim_folder, GOR, WCUT, icv_settings[0], icv_settings[1], icv_settings[2])
            #prod_generator(sim_folder, icv_start=icvs.icv_start(), icv_control=icv_control)
            
            #inje_generator(sim_folder)
            #sims.append(utils.run_imex_remote(sim_folder, see_log=False, verbose=True))    
            
    #while sims:
    #    for idx, sim in enumerate(sims):
    #        if sim.is_alive():
    #            pass
    #        else:
    #            del sims[idx]
    #            break
            
    for sim_folder in sim_folders:        
        utils.generate_report(sim_folder, True)
