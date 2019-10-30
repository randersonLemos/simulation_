# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:01:10 2019

@author: randerson
"""

import numpy

PRODS  =  ['PRK085', 'PRK084', 'PRK045', 'PRK083', 'PRK060', 'PRK028', 'PRK061', 'PRK014', 'PRK052', 'PWILDC']
NR_ICVS = [       3,        2,        3,        3,        2,        2,        3,        3,        2,        0]
            
def icv_start():
    dic = {}
    dic['PRK085'] = (2008.0, 183, 200)
    dic['PRK084'] = (2008.0, 183, 200)
    dic['PRK045'] = (2008.0, 183, 200)
    dic['PRK083'] = (2008.0, 183, 200)
    dic['PRK060'] = (2008.0, 183, 200)
    dic['PRK028'] = (2008.0, 183, 200)
    dic['PRK061'] = (2008.0, 183, 200)
    dic['PRK014'] = (2008.0, 183, 200)
    dic['PRK052'] = (2008.0, 183, 200)
    dic['PWILDC'] = ()
    return dic

def icv_control_incremental(gor, wcut, gor_ffactor, wcut_ffactor, nr_stages):
    actions = numpy.linspace(1.0, 0.0, nr_stages+1)[1:] # excluding the first element i.e. the number 1.0
    gor_factors = numpy.linspace(1.0, gor_ffactor, nr_stages)
    wcut_factors = numpy.linspace(1.0, wcut_ffactor, nr_stages)
    gors = []
    wcuts = []
    for gor_factor, wcut_factor in zip(gor_factors, wcut_factors):
        gors.append(gor*gor_factor)
        wcuts.append(wcut*wcut_factor)
        if wcut*wcut_factor > 100.0:
            wcuts.append(100.0)
    
    dic = {}
    for well, nr_icv in zip(PRODS, NR_ICVS):
        dic[well] = []
        for idx in range(nr_icv):
            conds = []
            layer = '{}_Z{}'.format(well,idx+1)
            for gor, wcu, act in zip(gors,wcuts,actions):
                gor_cond = "*ON_CTRLLUMP '{}' *GOR  > {}".format(layer, gor)
                wcu_cond = "*ON_CTRLLUMP '{}' *WCUT > {}".format(layer, wcu)
                conds.append((gor_cond, 'OR', wcu_cond, act,))
            dic[well].append(tuple(conds))
    return dic