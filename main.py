import pathlib
from settings import *
from run.scripts import imex
from well.scripts import wells, utils


def run_imex(idx, see_log=False, verbose=False):
    imexx = imex.IMEX(
              machine = MACHINE
            , exe = IMEX_EXE
            , dat_file = IMEX_FOLDER_DAT / 'sim_{:03d}'.format(idx) / 'main.dat'
            , output_folder = IMEX_FOLDER_OUT / 'sim_{:03d}'.format(idx)
            , user = USER
            , cluster_name = CLUSTER_NAME
            , queue_kind = QUEUE_KIND
            , see_log = see_log
            , verbose = verbose
            )
    imexx.run()
    return imexx


def generate_producers(idx):
    path = IMEX_FOLDER_OUT / 'sim_{:03d}'.format(idx)
    utils.create_dat_at('./well/_dat', str(path))

    Producer    = wells.Producer

    from well.scripts import producers_detail as pd

    keys        = PRODS_KEYS
    prods_names = PRODS_NAMES
    prods_times = PRODS_OPEN_TIMES
    icvs_qtyss  = PRODS_ICVS_QTYS

    ws = []
    for key in keys:
        w = Producer(name=prods_names[key], group='PRODUCTION')
        w.add_operate(maxmin='*MAX', con_type='*STL', value='6000.0', action='*CONT *REPEAT')
        w.add_operate(maxmin='*MIN', con_type='*BHP', value= '100.0', action='*CONT *REPEAT')
        w.add_monitor(monitor_type= '*WCUT', value='0.95', action='*SHUTIN *REPEAT')
        w.add_geometry(dir='*K', rw='0.108', geofac='0.370', wfrac='1.000', skin='0.000')
        w.add_perf(index_keyword='*GEOA', completion=getattr(pd, prods_names[key]))
        w.add_availability(avail='1.0')
        w.add_opening(timsim=prods_times[key])
        w.write_inc(path / 'wells')
        ws.append(w)
    return wells


if __name__ == '__main__':
    for i in range(10):
        generate_producers(i)
        run_imex(i, verbose=True)

