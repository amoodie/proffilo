__all__ = ['BaseObservations', 'SedimentConcentrationObservations', 'VelocityObservations']


import numpy as np
import pandas as pd
import abc

try:
    import matplotlib.pyplot as plt # Optional dependency
    from matplotlib import cm
except ImportError as e:
    plt = e

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
        self._set_data_init(data, connection)
        
        self.flow_depth = flow_depth
        

    @property
    def data(self):
        """`pd.DataFrame` : Pandas dataframe object containing the observation data.

        """
        return self._data


    def _set_data_init(self, data, connection):
        """Handle initiation of the pandas dataframe.

        """
        def __set_data_empty_DataFrame():
            df = pd.DataFrame(columns=self.columns)
            self._data = df
            self.has_data = False # for safety from overwriting

        def __set_data_from_DataFrame():
            """
            sets up self._data properly, expanding with empty columns, sets up mapper.
            """
            self._data = data.copy(deep=True)
            for c, col in enumerate(self.columns):
                if col not in self.data: # check if it's in data exactly
                    if col not in connection.keys(): # check if it's given in the connection
                        self._data[col] = np.nan # full_like(self.data) # add it
            self.has_data = True # for safety from overwriting

        def __set_connection():
            # loop through a second time to add anything in connection to the mapper
            for c, col in enumerate(self.columns):
                if col in connection.keys():
                    self._data.rename(columns={connection[col]: col}, inplace=True)
                    self.mapper[connection[col]] = col

        if type(data) is pd.DataFrame:
            __set_data_from_DataFrame()
        else:
            __set_data_empty_DataFrame()
        __set_connection()


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


    def __repr__(self):
        return str(self.data)


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

    @property
    @abc.abstractmethod
    def type(self):
        """
        type of Observation.
        """
        return self._type

    @type.setter
    def type(self, var):
        self._type = var

    @property
    @abc.abstractmethod
    def val(self):
        """Value of Observation.

        Should be overwritten to be whatever is most intuitve for the observation type.
        """
        return self._val

    @property
    @abc.abstractmethod
    def _display_units(self):
        """
        _display_units of Observation.
        """
        return self.__display_units

    @_display_units.setter
    def _display_units(self, var):
        self.__display_units = var

    def _attribute_checker(self, checklist):
        att_dict = {}
        assert type(checklist) is list, 'checklist must be of type `list`, but was type: %s' % type(checklist)
        for c, check in enumerate(checklist):
            has = getattr(self, check , None)
            if has is None:
                att_dict[check] = False
            else:
                att_dict[check] = True

        log_list = [value for value in att_dict.values()]
        log_form = [value for string, value in zip(log_list, att_dict.keys())  if not string]
        if not all(log_list):
            raise RuntimeError('required attribute(s) not assigned: '+str(log_form)+
                               ' for object: '+str(type(self)))
        return att_dict

    def _mpl_check(self):
        if isinstance(plt, ImportError):
            raise plt

    def show_profile(self, block=False, savestr=None, **kwargs):
        """Show observations as a profile.

        .. note:: This function requires `matplotlib`.

        Parameters
        ----------

        block : `bool`, optional
            Whether to pause script execution by showing the plot.
            I.e., the ``block`` argument in matplotlib's ``plt.show()``.

        savestr : `str`, optional
            String to save the output file. If given ``block`` is
            set to False.

        **kwargs : optional
            Any arbitrary ``matplotlib.pyplot.plot()`` keyword arguments for
            the plot specification.

        Returns
        -------

        None
        """
        self._mpl_check()

        xlab = kwargs.pop('xlabel', self.type+' ('+self._display_units+')')
        ylab = kwargs.pop('ylabel', 'distance above bed (m)')
        marker = kwargs.pop('marker', 'o')
        fillstyle = kwargs.pop('fillstyle', 'none')
        linestyle = kwargs.pop('linestyle', 'none')
        
        fig, ax = plt.subplots()
        ax.plot(self.val, self.z, marker=marker, fillstyle=fillstyle, 
                                  linestyle=linestyle, **kwargs)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        if savestr:
            fig.savefig(savestr)
            plt.show(block=block)
        else:
            plt.show()
        plt.close()



class SedimentConcentrationObservations(BaseObservations):
    """Sediment concentration observations collection.
    
    This class provides organization to concentration observations associated
    with a station. The class provides a number of convenient functions that
    help streamline organization and access of data associated with
    concentration observations. In particular, there are several routines for
    extracting information from :class:`~proffilo.distribution.Distributon`
    objects associated with concentration measurements.

    Notably, this class overloads :attr:`__getattr__`, such that column names
    defined in the :attr:`data` table can be directly accessed via, for
    example, ``self.concentration``. Additionally, all methods available to
    ``pandas.DataFrame`` should be accessible as normal, including: indexing
    (``.iloc``, ``.loc``) and assignment (``.at``, ``.where``).

    The class can be instantiated independent of a
    :class:`~proffilo.station.Station` object, but is usually assigned as an
    attribute of a Station object during regular use.

    Examples
    --------

    .. note::

        There is no support for indexing with original column labels via
        ``pd.DataFrame`` methods. For example, if an Observation class is
        initialized with the ``'concentration'`` field as ``'conc'`` in
        the dataframe, but linked via ``connection``, you cannot do
        ``stn.conc_obs.loc[:,'conc']``.
    """
    def __init__(self, data=None, flow_depth=None, connection={}):
        """Initialize a SedimentConcentrationObservations object.

        Parameters
        ----------

        data : `pandas.DataFrame`, optional
            An optional DataFrame with the concentration data preconfigured.
            If not supplied, this field is set to ``None``, and data can be
            filled in via the :attr:`add_observation` method.

        flow depth : `float`, optional.
            Flow depth [m]. Some functionality may be limited if this is not supplied.

        """
        columns = ['concentration', 'elevation', 'distribution']
        connection['elevation'] = 'z'
        super().__init__(columns, data, flow_depth, connection)

        self._val = self.concentration
        self.type = 'sediment concentration'
        self._display_units = '-'
        

    def add_observation(self, var):
        raise NotImplementedError

    @property
    def z_norm(self):
        """`ndarray` : Normalized observation elevation.

        Elevation value is normalized into the interval [0,1], by dividing
        :attr:`z` by the :attr:`flow_depth`. If :attr:`flow_depth` is type
        `None`, :attr:`z_norm` raises `RuntimeError`. 
        """
        self._attribute_checker(['flow_depth'])
        return self.elevation / self.flow_depth

    @property
    def z(self):
        """`float` : Observation elevations above the bed [m].

        Alias to :attr:`elevation`.
        """
        return self._z

    @property
    def elevation(self):
        """`float` : Observation elevations above the bed [m].
        """
        return self._elevation

    @property
    def concentration(self):
        """`float` : Observation concentrations [-].
        """
        return self._concentration

    @property
    def distribution(self):
        """`float` : Observation grain-size distributions [:class:`~proffilo.distribution.Distribution`].
        """
        return self._distribution

    def show_distributions(self, cumulative=False, block=False, savestr=None, **kwargs):
        """Show the grain-size distributions of the observation.
        
        Show the dirtubutions in a plot. 

        .. note:: This function requires `matplotlib`.

        Parameters
        ----------

        block : `bool`, optional
            Whether to pause script execution by showing the plot.
            I.e., the ``block`` argument in matplotlib's ``plt.show()``.

        savestr : `str`, optional
            String to save the output file. If given ``block`` is
            set to False.

        **kwargs : optional
            Any arbitrary ``matplotlib.pyplot.plot()`` keyword arguments for
            the plot specification. Note that these specs are passed to all lines.

        Returns
        -------

        None
        """
        self._mpl_check()

        xlab = kwargs.pop('xlabel', r'grain size ($\mu m$)')
        if cumulative:
            ylab = kwargs.pop('ylabel', 'percent finer (%)')
            ylim = (0, 100)
        else:
            ylab = kwargs.pop('ylabel', 'percent (%)')

        colmap = kwargs.pop('colmap', 'viridis')
        colormap = cm.get_cmap(colmap, 32)

        fig, ax = plt.subplots()

        for d, ddist in enumerate(self.distribution):
            if cumulative:
                __dist = ddist.cumulative_dist
            else:
                __dist = ddist.dist
            ax.plot(ddist.bin, __dist, **kwargs)
    
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        if savestr:
            fig.savefig(savestr)
            plt.show(block=block)
        else:
            plt.show()
        plt.close()



class VelocityObservations(BaseObservations):
    """Velocity concentration observations collection.
    
    .. note::

        There is no support for indexing with original column labels via
        ``pd.DataFrame`` methods. For example, if an Observation class is
        initialized with the ``'concentration'`` field as ``'conc'`` in
        the dataframe, but linked via ``connection``, you cannot do
        ``stn.conc_obs.loc[:,'conc']``.
    """
    def __init__(self, data=None, flow_depth=None, connection={}):
        """Initialize a VelocityObservations object.

        Parameters
        ----------

        data : `pandas.DataFrame`, optional
            An optional DataFrame with the observation data preconfigured.
            If not supplied, this field is set to ``None``, and data can be
            filled in via the :attr:`add_observation` method.

        flow depth : `float`, optional.
            Flow depth [m]. Some functionality may be limited if this is not supplied.

        """
        columns = ['velocity', 'elevation']
        connection['elevation'] = 'z'
        super().__init__(columns, data, flow_depth, connection)

        self.type = 'velocity'
        
    def add_observation(self, var):
        raise NotImplementedError

    @property
    def z_norm(self):
        """`ndarray` : Normalized observation elevation.

        Elevation value is normalized into the interval [0,1], by dividing
        :attr:`z` by the :attr:`flow_depth`. If :attr:`flow_depth` is type
        `None`, :attr:`z_norm` raises `RuntimeError`. 
        """
        self._attribute_checker(['flow_depth'])
        return self.elevation / self.flow_depth

    @property
    def z(self):
        """`float` : Observation elevations above the bed [m].

        Alias to :attr:`elevation`.
        """
        return self._z

    @property
    def elevation(self):
        """`float` : Observation elevations above the bed [m].
        """
        return self._elevation
