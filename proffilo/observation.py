__all__ = ['BaseObservations', 'SedimentConcentrationObservations']


import numpy as np
import pandas as pd
import abc

class BaseObservations(object):
    """Base observations collection class.

    .. warning::

        This class should **never** be instantiated directly.

    """
    def __init__(self, columns, data=None, flow_depth=None, connection={}):
        """
        Initialize the BaseObservations object.

        Parameters
        ----------
        z : `float`
            Elevation of observation above the bed [m]. Must be greater than
            zero and less than the flow depth, if provided.

        flow depth : `float`, optional
            Flow depth [None]. If not provided, some methods may be unavailable.

        """
        self.columns = columns
        self.mapper = {} # internal connections list

        self.has_data = False # for safety from overwriting
        self._data = [] # need to init for __getattribute__
        if type(data) is pd.DataFrame:
            self._set_data_from_DataFrame(data, connection)
        else:
            self._set_data_empty_DataFrame()

        self.flow_depth = flow_depth
        

    @property
    def data(self):
        return self._data

    def _set_data_empty_DataFrame(self, data, connection):
        df = pd.DataFrame(columns=self.columns)
        self._data = df
        self.has_data = False # for safety from overwriting


    def _set_data_from_DataFrame(self, data, connection):
        """
        sets up self._data properly, expanding with empty columns, sets up mapper.
        """
        self._data = data.copy(deep=True)
        for c, col in enumerate(self.columns):
            if col not in self.data: # check if it's in data exactly
                if col not in connection.keys(): # check if it's given in the connection
                    self._data[col] = np.nan # full_like(self.data) # add it

        # loop through a second time to add anything in connection to the mapper
        for c, col in enumerate(self.columns):
            if col in connection.keys():
                self._data.rename(columns={connection[col]: col}, inplace=True)
                self.mapper[connection[col]] = col

        self.has_data = True # for safety from overwriting

    def __getattr__(self, name):
        """Make columns and DataFrame methods directly accessible.

        This overloads ``__getattr__`` to look for undefined attributes as
        columns in :attr:`self.data`. If found, returns the column values as an `ndarray`.

        If not found, look for it as a method of ``pandas.DataFrame``. If found, execute.
        """
        if name in self.data:
            return self.data[name].values
        elif name in self.mapper.keys():
            return self.data[self.mapper[name]].values
        else:
            try:
                return getattr(self.data, name)
            except AttributeError as e:
                raise e # AttributeError('Observation class has no attribute: %s' % name)

    @property
    def flow_depth(self):
        """`float` : Flow depth [m].
        """
        return self._flow_depth

    @flow_depth.setter
    def flow_depth(self, var):
        if var:
            assert var > 0, 'Flow depth must be > 0, but was: %s' % str(var)
            self._flow_depth = var
        else:
            self._flow_depth = None



class SedimentConcentrationObservations(BaseObservations):
    """Sediment concentration observations collection.
    
    .. warning::

            There is no support for indexing with original column labels via
            ``pd.DataFrame`` methods. For example, if an Observation class is
            initialized with the ``'concentration'`` field as ``'conc'`` in
            the dataframe, but linked via ``connection``, you cannot do
            ``stn.conc_obs.loc[:,'conc']``.
    """
    def __init__(self, data=None, flow_depth=None, connection={}):
        """Initialize a ConcentrationObservation.

        Parameters
        ----------

        data : `pandas.DataFrame`, optional
            An optional DataFrame with the concentration data preconfigured.
            If not supplied, this field is set to ``None``, and data can be
            filled in via the :attr:`add_observation` method.

        flow depth : `float`, optional.
            Flow depth [m]. Some functionality may be limited if this is not supplied.

        distribution : :class:`~proffilo.distribution.Distribution`, optional
            A Distribution describing the observation.

        """
        columns = ['concentration', 'elevation', 'distribution']
        connection['elevation'] = 'z'
        super().__init__(columns, data, flow_depth, connection)

        self.type = 'sediment_concentration'
        

    def add_observation(self, var):
        self.columns


    # @property
    # def z(self):
    #     """`float` : Observation elevation [m].

    #     Elevation of observation above the bed [m]. Must be greater than 0.
    #     """
    #     return self._z

    # @property
    # def z_norm(self):
    #     """`ndarray` : Normalized observation elevation.

    #     Elevation value is normalized into the interval [0,1], by dividing
    #     :attr:`z` by the :attr:`flow_depth`. If :attr:`flow_depth` is type
    #     `None`, :attr:`z_norm` is set to `None`. 
    #     """
    #     return self._z_norm

    # @z.setter
    # def z(self, var):
    #     assert var > 0, 'Observation ``z`` must be > 0, but was: %s' % str(var)
    #     self._z = var
    #     if self.flow_depth:
    #         _norm = var / self.flow_depth
    #         assert _norm[0] >= 0 and _norm[-1] <= 1
    #         self._z_norm = _norm
    #     else:
    #         self._z_norm = None


"""
Initialize a ConcentrationObservation.

Parameters
----------
z : `float`
    Observation distance above the bed [m].

value : `numeric`, `ndarray`
    Value of the observation. Can be a single numeric value (i.e., a
    `int`, `float`), or list of values (i.e., a `list`, `ndarray`). If
    a list is supplied, the first value describes the mean value of
    the sample, and the second describes uncertainty.
"""