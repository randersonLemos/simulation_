import pathlib
from settings import *
from run.scripts import imex
from well.scripts import wells, utils


def run_imex(idx, see_log=False, verbose=False):
    imexx = imex.IMEX(
              machine = MACHINE
            , exe = IMEX_EXE
            , dat_file = ROOT / IMEX_FOLDER_DAT / 'sim_{:03d}'.format(idx) / 'main.dat'
            , output_folder = ROOT / IMEX_FOLDER_OUT / 'sim_{:03d}'.format(idx)
            , user = USER
            , cluster_name = CLUSTER_NAME
            , queue_kind = QUEUE_KIND
            , see_log = see_log
            , verbose = verbose
            )
    imexx.run()
    return imexx


def generate_producers(idx, verbose=False):
    path = Path(ROOT / IMEX_FOLDER_OUT / 'sim_{:03d}'.format(idx))
    if MACHINE == 'remote':
        path = Path(ROOT_LOCAL / IMEX_FOLDER_OUT / 'sim_{:03d}'.format(idx))
    if verbose: print('generate_producers path:\n\t{}'.format(path))
    path.mkdir(parents=True, exist_ok=True)
    utils.create_dat_at('./well/_dat', str(path))

    from well.scripts import producers_detail as pd

    Producer    = wells.Producer

    keys        = PRODS_KEYS
    prods_names = PRODS_NAMES
    prods_times = PRODS_OPEN_TIMES

    ws = []
    for key in keys:
        w = Producer(name=prods_names[key], group='PRODUCTION')
        w.add_operate(maxmin='*MAX', con_type='*STL', value='3000.0', action='*CONT *REPEAT')
        w.add_operate(maxmin='*MIN', con_type='*BHP', value= '295.0', action='*CONT *REPEAT')
        w.add_monitor(monitor_type= '*WCUT', value='0.95', action='*SHUTIN *REPEAT')
        w.add_geometry(dir='*K', rw='0.108', geofac='0.370', wfrac='1.000', skin='0.000')
        w.add_perf(index_keyword='*GEOA', completion=getattr(pd, prods_names[key]))
        w.add_availability(avail='1.0')
        w.add_opening(timsim=prods_times[key])
        w.write_inc(path / 'wells')
        ws.append(w)
    return ws


def generate_injectors(idx, verbose=True):
    path = Path(ROOT / IMEX_FOLDER_OUT / 'sim_{:03d}'.format(idx))
    if MACHINE == 'remote':
        path = Path(ROOT_LOCAL / IMEX_FOLDER_OUT / 'sim_{:03d}'.format(idx))
    if verbose: print('generate_injectors path:\n\t{}'.format(path))
    path.mkdir(parents=True, exist_ok=True)
    utils.create_dat_at('./well/_dat', str(path))

    from well.scripts import injectors_detail as idd

    Injector_WAG = wells.Injector_WAG

    keys = INJES_KEYS
    injs_names = INJES_NAMES
    injs_times = INJES_OPEN_TIMES
    injs_wagss = INJES_WAGSS

    ws = []
    for key in keys:
        w = Injector_WAG(name=injs_names[key], group='INJECTION')
        w.add_operate(which_mode='GAS', maxmin='*MAX', con_type='*STG', value='3000000.0', action='*CONT *REPEAT')
        w.add_operate(which_mode='GAS', maxmin='*MAX', con_type='*BHP', value='540.0'    , action='*CONT *REPEAT')
        w.add_operate(which_mode='WATER', maxmin='*MAX', con_type='*STW', value='5000.0', action='*CONT *REPEAT')
        w.add_operate(which_mode='WATER', maxmin='*MAX', con_type='*BHP', value='470.0' , action='*CONT *REPEAT')
        w.add_geometry(dir='*K', rw='0.108', geofac='0.370', wfrac='1.000', skin='0.000')
        w.add_perf(index_keyword='*GEOA', completion=getattr(idd, injs_names[key]))
        w.add_availability(avail='1.0')
        w.add_opening(which_mode=injs_times[key][0], timsim=injs_times[key][1])
        w.add_wag_strategy(start_mode=injs_wagss[key], timsim='1918.0', delta_timsim='180.0'
                , apply_times='100', increment='366')
        w.write_inc(path / 'wells')
        ws.append(w)
    return ws


if __name__ == '__main__':
    for i in range(3):
        generate_producers(i, verbose=True)
        generate_injectors(i, verbose=True)
    for i in range(3):
        run_imex(i, see_log=True, verbose=True)