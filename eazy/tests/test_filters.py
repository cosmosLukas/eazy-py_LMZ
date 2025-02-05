import pytest
import os

import numpy as np

from .. import utils
from .. import filters

def test_array_filter():
    """
    Generate filter from arrays
    """
    wx = np.arange(5400, 5600., 1)
    wy = wx*0.
    wy[10:-10] = 1
    
    f1 = filters.FilterDefinition(wave=wx, throughput=wy)
    print('xxx', f1.pivot)
    assert(np.allclose(f1.pivot, 5500, rtol=1.e-3))
    assert(np.allclose(f1.ABVega, 0.016, atol=0.03))
    assert(np.allclose(f1.equivwidth, 180))
    assert(np.allclose(f1.rectwidth, 180))

def test_pysynphot_filter():
    """
    PySynphot filter bandpass
    """
    try:
        import pysynphot as S
    except:
        return True
    
    v_pysyn = S.ObsBandpass('v')
    v_eazy = filters.FilterDefinition(bp=v_pysyn)
    
    assert(np.allclose(v_pysyn.pivot(), v_eazy.pivot, rtol=0.001))
    
def test_data_path():
    """
    Data path
    """
    path = os.path.join(os.path.dirname(__file__), '../data/')
    assert(os.path.exists(path))
    return path

def test_read_filter_res():
    """
    Read FILTER.RES
    """
    data_path = test_data_path()
    filter_file = os.path.join(data_path, 'filters/FILTER.RES.latest')
    res = filters.FilterFile(filter_file)
    
    assert(res[155].name.startswith('REST_FRAME/maiz-apellaniz_Johnson_V'))
    assert(np.allclose(res[155].pivot, 5479.35, rtol=0.001))
    return res