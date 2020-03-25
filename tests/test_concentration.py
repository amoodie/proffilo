import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np

from proffilo import concentration


def test_cvtm_zero():
    _result = concentration.convert_volumetric_to_mass(0.000, 2650)
    assert _result == 0

def test_cvtm_example():
    _result = concentration.convert_volumetric_to_mass(0.0003, 2650)
    assert _result == pytest.approx(0.7949999)

def test_cmtv_zero():
    _result = concentration.convert_mass_to_volumetric(0.000, 2650)
    assert _result == 0

def test_cmtv_example():
    _result = concentration.convert_mass_to_volumetric(2, 2650)
    assert _result == pytest.approx(0.000754716981132)
    