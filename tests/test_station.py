import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np

from proffilo.distribution import Distribution
from proffilo.station import Station

ones = np.ones((12,2))
dist = Distribution(arr=ones)


def test_init_blank():
    stn = Station(Distribution)
