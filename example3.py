import settings as sett            
from run2 import imex, report

def generate_producers(operates, monitor, well_completion, well_opening, well_on_time, icv_layerclump, icv_start, icv_control, output_folder):
    from well2 import frames
    from well2 import utils
    import pathlib
    
    for key in well_completion:
        p = frames._Frame_Prod_Dual(key, 'PRODUCTION')
        for ope in operate: p.get_operate(*ope)
        for mon in monitor: p.get_monitor(*mon)                
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
    
def generate_wells(operates, monitor, sim_folder):
    import well2.infos1 as infos1
    generate_producers(
          operates
        , monitor
        , infos1.well_completion
        , infos1.well_opening
        , infos1.well_on_time
        , infos1.icv_layerclump
        , infos1.icv_start
        , infos1.icv_control
        , sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder / 'wells'
        )   
    
    import well2.infos2 as infos2
    generate_injectors_wag(
          infos2.well_completion
        , infos2.well_opening
        , infos2.well_on_time
        , infos2.well_wag
        , sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder / 'wells'
        )

def simulation(sim_folder):
    root = sett.ROOT_LOCAL
    if sett.MACHINE == 'remote': root = sett.ROOT_REMOTE
    imexx = imex.IMEX(            
          sett.MACHINE
        , sett.IMEX_EXE
        , root / sett.MAIN_FOLDER / sim_folder / sett.DAT_FILE
        , root / sett.MAIN_FOLDER / sim_folder
        , sett.USER
        , sett.CLUSTER_NAME
        , sett.QUEUE_KIND
        , see_log = False
        , verbose = True
        )
    imexx.run()
    return imexx
    
def generate_report(sim_folder):
    repor = report.REPORT(
          exe = sett.REPORT_EXE
        , irf_file = sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder / sett.IRF_FILE
        , output_folder = sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder
        , verbose = True
        )
    repor.run()

def some_settings(sim_folder):
    from distutils.file_util import copy_file
    from distutils.dir_util import copy_tree   
    
    (sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder).mkdir(parents=True, exist_ok=True)
    (sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder / 'includes').mkdir(parents=True, exist_ok=True)
    
    copy_file(str(sett.ROOT_LOCAL / 'dat2' / sett.DAT_FILE), str(sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder))
    copy_tree(str(sett.ROOT_LOCAL / 'dat2' / 'includes'), str(sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder / 'includes')) 
    
if __name__ == '__main__':   
    import numpy
    import itertools
    temp1 = [('*MAX', '*STL', val, '*CONT *REPEAT') for val in numpy.linspace(2000,5000,10)]
    temp2 = [('*MIN', '*BHP', val, '*CONT *REPEAT') for val in numpy.linspace(150,450,10)]
    operates = list(itertools.product(temp1, temp2))
    monitor = [('*WCUT', 0.95, '*SHUTIN')]
        
    sims = []
    for idx, operate in enumerate(operates):
        sim_folder = 'sim_{:03d}'.format(idx)   
        some_settings(sim_folder)
        generate_wells(operate, monitor, sim_folder)            
        sims.append(simulation(sim_folder))