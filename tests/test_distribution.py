import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np

from proffilo.distribution import Distribution


def test_init_null_array():
    ones = np.ones((12,2))
    dist = Distribution(arr=ones)

    assert dist.data[0,0] == ones[0,0]
