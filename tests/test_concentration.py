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
    
def test_cmtv_density_1000():
    _result = concentration.convert_mass_to_volumetric(2, 1000)
    assert _result == pytest.approx(0.002)

@pytest.mark.xfail(raises=ValueError)
def test_cmtv_density_0():
    _result = concentration.convert_mass_to_volumetric(2, 0)

@pytest.mark.xfail(raises=TypeError)
def test_cmtv_type_None():
    _result = concentration.convert_mass_to_volumetric(None, 1)

def test_cvtm_density_1000():
    _result = concentration.convert_volumetric_to_mass(2, 1000)
    assert _result == pytest.approx(2000)

@pytest.mark.xfail(raises=ValueError)
def test_cvtm_density_0():
    _result = concentration.convert_volumetric_to_mass(2, 0)

@pytest.mark.xfail(raises=TypeError)
def test_cvtm_type_None():
    _result = concentration.convert_volumetric_to_mass(None, 1)
