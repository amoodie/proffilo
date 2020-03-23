import numpy as np 

try:
    import matplotlib.pyplot as plt # Optional dependency
except ImportError as e:
    plt = e


class Distribution(object):
    """Grain-size distibution.

    Grain-size distribution class. Provides convenient organization and
    features, such as summarizing, or plotting.

    Attributes
    ----------
    bin : `ndarray`
        Grain-size bins characterizing the grain-size distribution.
    dist : `ndarray`
        Percentage of grain-size distribution in each bin.
    units : `str`
        Units of grain size [:math:`\mu` m]
    cumulative_dist : `ndarray`
        Cumulative percentage of grain-size distribution along bins. 

    """
    def __init__(self, arr, units='microns'):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note
        ----
        Do not include the `self` parameter in the ``Parameters`` section.

        Parameters
        ----------
        param1 : str
            Description of `param1`.
        param2 : list(str)
            Description of `param2`. Multiple
            lines are supported.
        param3 : :obj:`int`, optional
            Description of `param3`.

        """
        self.data = arr
        self.bin = self.data[:,0]
        self.dist = self.data[:,1]
        self.cumulative_dist = np.cumsum(self._dist)
        self.units = units


    @property
    def data(self):
        """
        Properties created with the ``@property`` decorator should be documented
        in the property's getter method.
        """
        return self._data

    @data.setter
    def data(self, var):
        if type(var) is list:
            var = np.array(var)
        self._data = var

        
    @property
    def bin(self):
        return self._bin

    @bin.setter
    def bin(self, var):
        if type(var) is list:
            var = np.array(var)
        assert var.ndim == 1
        self._bin = var

        
    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, var):
        if type(var) is list:
            var = np.array(var)
        assert var.ndim == 1
        assert np.sum(var) > 1, 'data must be supplied as percent, not fractional'
        assert np.sum(var) <= 100, 'data must be supplied as percent'
        self._dist = var


    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, var):
        if type(var) is list:
            var = np.array(var)
        self._units = var
        if self._units in ['microns', 'micron', 'mum', r'\mum', 'mu m']:
            self.display_units = r'$\mu$m'
        elif self._units in ['phi', r'\phi']:
            raise NotImplementedError('Other units not functional. Submit a PR!')
            self.display_units = r'$\phi$'


    @property
    def cumulative_dist(self):
        return self._cumulative_dist

    @cumulative_dist.setter
    def cumulative_dist(self, var):
        self._cumulative_dist = var


    def __repr__(self):
        return str(self.data)

        
    def d(self, x, units='microns'):
        assert x >= 0 and x <= 100, 'x must be in [0, 100], but was %s' % str(x)
        assert units == 'microns', 'NotImplemented for units other than microns'
        _val = np.interp(x, self.cumulative_dist, self.bin)
        # utils.coerce_to_unit()
        return  _val


    def _mpl_check(self):
        if isinstance(plt, ImportError):
            raise plt

    def show_distribution(self, cumulative=False, block=False, savestr=None, **kwargs):
        """
        Show the distribution
        """
        self._mpl_check()

        xlab = kwargs.pop('xlabel', 'grain size ('+self.display_units+')')
        if cumulative:
            __dist = self.cumulative_dist
            ylab = kwargs.pop('ylabel', 'percent finer (%)')
        else:
            __dist = self.dist
            ylab = kwargs.pop('ylabel', 'percent (%)')

        fig, ax = plt.subplots()
        ax.plot(self.bin, __dist, **kwargs)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        if savestr:
            fig.savefig(savestr)
            plt.show(block=block)
        else:
            plt.show()
