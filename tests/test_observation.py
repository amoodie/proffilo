import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np
import pandas as pd

from proffilo import observation

test_table = pd.DataFrame([[0.0003, 0.12], [0.0004, 0.12], 
                           [0.0002, 0.7], [0.00012, 1.1], 
                           [0.00004, 2.3]],
                   columns=['concentration', 'elevation'])
test_table_mismatch = pd.DataFrame([[0.0003, 0.12], [0.0004, 0.12], 
                           [0.0002, 0.7], [0.00012, 1.1], 
                           [0.00004, 2.3]],
                   columns=['conc', 'elevation'])


def test_SedimentConcentrationObservations_table_noconnection_match():
    conc_obs = observation.SedimentConcentrationObservations(data=test_table)
    assert type(conc_obs._data) is pd.DataFrame
    assert conc_obs._data.shape[0] == 5
    assert conc_obs._data.shape[1] == 3

def test_SedimentConcentrationObservations_table_noconnection_mismatch():
    conc_obs = observation.SedimentConcentrationObservations(data=test_table_mismatch)
    assert type(conc_obs._data) is pd.DataFrame
    assert conc_obs._data.shape[0] == 5
    assert conc_obs._data.shape[1] == 4

def test_SedimentConcentrationObservations_table_noconnection_asDFmethod():
    conc_obs = observation.SedimentConcentrationObservations(data=test_table)
    assert type(conc_obs._data) is pd.DataFrame
    assert conc_obs._data.shape[0] == 5
    assert conc_obs._data.shape[1] == 3

def test_SedimentConcentrationObservations_table_connection():
    connection = {'concentration': 'conc'}
    conc_obs = observation.SedimentConcentrationObservations(data=test_table_mismatch, connection=connection)
    assert type(conc_obs._data) is pd.DataFrame
    assert conc_obs._data.shape[0] == 5
    assert conc_obs._data.shape[1] == 3

def test_SedimentConcentrationObservations_table_emptyconnection():
    connection = {}
    conc_obs = observation.SedimentConcentrationObservations(data=test_table_mismatch, connection=connection)
    assert type(conc_obs._data) is pd.DataFrame
    assert conc_obs._data.shape[0] == 5
    assert conc_obs._data.shape[1] == 4

def test_SedimentConcentrationObservations_table_index_loc():
    connection = {'concentration': 'conc'}
    conc_obs = observation.SedimentConcentrationObservations(data=test_table_mismatch, connection=connection)
    returned = conc_obs.loc[:, 'concentration']
    assert len(returned) == conc_obs.shape[0]
    assert returned[0] == test_table_mismatch.loc[0, 'conc']

def test_SedimentConcentrationObservations_table_index_direct():
    connection = {'concentration': 'conc'}
    conc_obs = observation.SedimentConcentrationObservations(data=test_table_mismatch, connection=connection)
    returned = conc_obs.concentration
    assert len(returned) == conc_obs.shape[0]
    assert returned[0] == test_table_mismatch.loc[0, 'conc']

def test_SedimentConcentrationObservations_table_index_direct_connection():
    connection = {'concentration': 'conc'}
    conc_obs = observation.SedimentConcentrationObservations(data=test_table_mismatch, connection=connection)
    returned = conc_obs.conc
    assert len(returned) == conc_obs.shape[0]
    assert returned[0] == test_table_mismatch.loc[0, 'conc']

def test_SedimentConcentrationObservations_table_index_direct_connection_inclass():
    connection = {'concentration': 'conc'}
    conc_obs = observation.SedimentConcentrationObservations(data=test_table_mismatch, connection=connection)
    returned = conc_obs.z
    assert len(returned) == conc_obs.shape[0]
    assert returned[0] == test_table_mismatch.loc[0, 'elevation']
