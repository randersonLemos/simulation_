import log
from settings import *
from run.scripts import imex, report
from itertools import cycle
 
def generate_producers(well_completion, well_opening, well_on_time, icv_layerclump, icv_start, icv_control, output_folder):
    from well2 import frames
    from well2 import utils
    import pathlib

    for key in well_completion:
        p = frames._Frame_Prod_Dual(key, 'PRODUCTION')
        p.get_operate('*MAX', '*STL', 3000.0, '*CONT *REPEAT')
        p.get_operate('*MIN', '*BHP',  295.0, '*CONT *REPEAT')
        p.get_monitor('*WCUT', 0.95, '*SHUTIN')
        p.get_geometry('*K',0.108,0.370,1.0,0.0)
        p.get_perf('*GEOA')

        for com in utils.txt_to_lst(well_completion[key]):
            p.get_completion(com)

        p.get_on_time(well_on_time[key])
        p.get_open(well_opening[key])

        for lay in icv_layerclump[key]:
            p.get_layerclump(lay)

        #p.get_icv_start(icv_start[key])
        #p.get_icv_control(icv_control[key])

        p.build()
        p.write(pathlib.Path(output_folder) / '{}.inc'.format(key))

def generate_injectors_wag(well_completion, well_opening, well_on_time, well_wag, output_folder):
    from well2 import frames
    from well2 import utils
    import pathlib
    for key in well_completion:
        i = frames._Frame_Inje_Dual_Wag(key, 'INJECTION')
        i.get_operate('G','*MAX','*STG',3000000.0,'*CONT REPEAT')
        i.get_operate('G','*MAX','*BHP',    540.0,'*CONT REPEAT')
        i.get_operate('W','*MAX','*STW',   5000.0,'*CONT REPEAT')
        i.get_operate('W','*MAX','*BHP',    470.0,'*CONT REPEAT')
        i.get_geometry('*K',0.108,0.370,1.0,0.0)
        i.get_perf('*GEOA')

        for com in utils.txt_to_lst(well_completion[key]):
            i.get_completion(com)

        i.get_on_time(well_on_time[key])
        i.get_open(*well_opening[key])

        i.get_wag(*well_wag[key])

        i.build()
        i.write(pathlib.Path(output_folder) / '{}.inc'.format(key))
           
if __name__ == '__main__':   
    import settings as sett            
    idx = 1
    import well2.infos1 as infos1
    generate_producers(infos1.well_completion
        , infos1.well_opening
        , infos1.well_on_time
        , infos1.icv_layerclump
        , infos1.icv_start
        , infos1.icv_control
        , sett.ROOT / sett.IMEX_FOLDER_DAT / 'sim_{:03d}'.format(idx) / 'wells'
        )   
    
    import well2.infos2 as infos2
    generate_injectors_wag(
          infos2.well_completion
        , infos2.well_opening
        , infos2.well_on_time
        , infos2.well_wag
        , sett.ROOT / sett.IMEX_FOLDER_DAT / 'sim_{:03d}'.format(idx) / 'wells'
        )
     
    root = sett.ROOT_LOCAL
    if sett.MACHINE == 'remote': root = sett.ROOT_REMOTE
    imexx = imex.IMEX(            
          sett.MACHINE
        , sett.IMEX_EXE
        , root / sett.IMEX_FOLDER_DAT / 'sim_{:03d}'.format(idx) / 'main.dat'
        , root / sett.IMEX_FOLDER_OUT / 'sim_{:03d}'.format(idx)
        , sett.USER
        , sett.CLUSTER_NAME
        , sett.QUEUE_KIND
        , see_log = True
        , verbose = True
        )
    imexx.run()
    
    repor = report.REPORT(
          exe = sett.REPORT_EXE
        , irf_file = sett.ROOT_LOCAL / sett.REPORT_FOLDER_IRF / 'sim_{:03d}'.format(idx) / 'main.irf'
        , output_folder = sett.ROOT_LOCAL / sett.REPORT_FOLDER_OUT / 'sim_{:03d}'.format(idx)
        , verbose = True
        )
    repor.run()