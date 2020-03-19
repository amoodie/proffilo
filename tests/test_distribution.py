import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np

from proffilo.distribution import Distribution

bins = np.linspace(10, 500, 50).T
vals = np.linspace(0, 100, 50)
vals[1:] = vals[1:]-vals[:-1]
arr = np.column_stack((bins, vals))
lindist = Distribution(arr=arr)

def test_init_null_array():
    ones = np.ones((12,2))
    dist = Distribution(arr=ones)

    assert dist.data[0,0] == ones[0,0]

def test_lindist_validate():
    assert lindist.bin[0] == 10
    assert lindist.bin[-1] == 500

def test_d_function():
    assert lindist.d(90) == 451
    assert lindist.d(84) == pytest.approx(421.59999)
