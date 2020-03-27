__all__ = ['BaseObservations', 'SedimentConcentrationObservations']


import numpy as np
import pandas as pd
import abc

class BaseObservations(object):
    """Base observations collection class.

    .. warning::

        This class should **never** be instantiated directly.

    """
    def __init__(self, z=None, flow_depth=None):
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
        self.flow_depth = flow_depth
        self.z = z

    @property
    def flow_depth(self):
        """`float` : Flow depth [m].
        """
        return self._flow_depth

    @flow_depth.setter
    def flow_depth(self, var):
        if var:
            # assert var > 0, 'Observation ``z`` must be > 0, but was: %s' % str(var)
            self._flow_depth = var
        else:
            self._flow_depth = None

    @property
    def z(self):
        """`float` : Observation elevation [m].

        Elevation of observation above the bed [m]. Must be greater than 0.
        """
        return self._z

    @property
    def z_norm(self):
        """`ndarray` : Normalized observation elevation.

        Elevation value is normalized into the interval [0,1], by dividing
        :attr:`z` by the :attr:`flow_depth`. If :attr:`flow_depth` is type
        `None`, :attr:`z_norm` is set to `None`. 
        """
        return self._z_norm

    @z.setter
    def z(self, var):
        assert var > 0, 'Observation ``z`` must be > 0, but was: %s' % str(var)
        self._z = var
        if self.flow_depth:
            _norm = var / self.flow_depth
            assert _norm[0] >= 0 and _norm[-1] <= 1
            self._z_norm = _norm
        else:
            self._z_norm = None


    @property
    @abc.abstractmethod
    def val(self):
        """`None` : Observation value.

        Value of observation, should be overwritten by subclasses to handle
        various datatypes.
        """
        return self._val

    @val.setter
    def val(self, var):
        self._val = var

    class AttributeArray(object):
        """Agnostic attribute.

        An agnostic attribute class that wraps the pandas DataFrame.
        """
        def __init__(self, name, columns):
            self.name = name
            if type(columns) is list:
                self.data = pd.DataFrame(columns=columns)
            else:
                raise ValueError('`columns` must be type `list`.')

        def append(self, var):
            self.data = np.append(self.data, var)

        def replace(self):
            raise NotImplementedError

        def delete(self):
            raise NotImplementedError

        def __getitem__(self, sliced):
            print(sliced)
            return 10

        def __len__(self):
            return len(self.data)

        def where(self, arg):
            fart=3
            print(eval(arg))


class SedimentConcentrationObservations(BaseObservations):
    """Sediment concentration observations collection.
    
    """
    def __init__(self, z=1, value=None, flow_depth=None, distribution=None):
        """Initialize a ConcentrationObservation.
        
        Parameters
        ----------
        z : `float`
            Observation distance above the bed [m].

        value : `numeric`, `ndarray`
            Value of the observation. Can be a single numeric value (i.e., a
            `int`, `float`), or list of values (i.e., a `list`, `ndarray`). If
            a list is supplied, the first value describes the mean value of
            the sample, and the second describes uncertainty.

        flow depth : `float`, optional.
            Flow depth [m]. Some functionality may be limited if this is not supplied.

        distribution : :class:`~proffilo.distribution.Distribution`, optional
            A Distribution describing the observation.

        """
        super().__init__(z, flow_depth)

        # raise NotImplementedError

        self.type = 'sediment_concentration'
        self.columns = ['concentration', 'elevation', 'distribution', 'test1']
        self.concentration = self.AttributeArray('concentration', self.columns)


    def add_observation(self, var):
        self.columns


    @property
    def concentration(self):
        return self._concentration

    @concentration.setter
    def concentration(self, var):
        self._concentration = var

    