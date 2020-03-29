import numpy as np
from scipy import stats

try:
    import matplotlib.pyplot as plt # Optional dependency
except ImportError as e:
    plt = e


class Distribution(object):
    """Grain-size distibution.

    Grain-size distribution class. Provides convenient organization and
    features, such as summarizing, or plotting.
    
    """
    def __init__(self, arr, is_cumulative=False, units='microns'):
        """Intialize a Distribution.

        Parameters
        ----------
        arr : `ndarray`
            An Mx2 `ndarray` where the first column is the grain size bins,
            and the second column is the distribution values. If the second
            column is specified as a cumulative distribution give
            `is_cumulative` as True.
        
        is_cumulative : `bool`, optional
            Boolean specifying whether the second column of `arr`.

        units : `str`, optional
            Units of the grain size bins, only supports ``'microns'``.
        """

        self.data = (arr.copy(), is_cumulative)
        self.units = units


    @property
    def data(self):
        """
        Properties created with the ``@property`` decorator should be documented
        in the property's getter method.
        """
        return self._data

    @data.setter
    def data(self, var, is_cumulative=False):
        try:
            _data, _is_cumulative = var
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        if type(_data) is list:
            _data = np.array(_data)
        if _is_cumulative:
            # _data = _data.copy()
            _data[1:,1] = _data[1:,1]-_data[:-1,1]
            _data[0,1] = np.nan
        self._data = _data
        self.bin = self.data[:,0]
        self.dist = self.data[:,1]

        
    @property
    def bin(self):
        """`ndarray` : Distribution bins [:math:`\\mu` m].

        Grain-size bins characterizing the grain-size distribution.
        """
        return self._bin

    @bin.setter
    def bin(self, var):
        if type(var) is list:
            var = np.array(var)
        assert var.ndim == 1
        self._bin = var

        
    @property
    def dist(self):
        """`ndarray` : Percentage in each bin [%].

        Percentage of grain-size distribution in each bin.
        """
        return self._dist

    @dist.setter
    def dist(self, var):
        if type(var) is list:
            var = np.array(var)
        assert var.ndim == 1
        assert np.nansum(var) > 1, 'data must be supplied as percent, not fractional'
        assert np.nansum(var) <= 100, 'data must be supplied as percent'
        self._dist = var
        self.cumulative_dist = np.nancumsum(self._dist)


    @property
    def units(self):
        """`str` : Units of bins.

        Units of grain size [:math:`\mu` m]
        """
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
        else:
            raise ValueError('Bad units supplied: %s' % self._units)


    @property
    def cumulative_dist(self):
        """`ndarray` : Cumulative distribution.

        Cumulative percentage of grain-size distribution along bins [%]. 
        """
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
            ylim = (0, 100)
        else:
            __dist = self.dist
            ylab = kwargs.pop('ylabel', 'percent (%)')

        fig, ax = plt.subplots()
        ax.plot(self.bin, __dist, **kwargs)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        if cumulative:
            ax.set_ylim(ylim)
        if savestr:
            fig.savefig(savestr)
            plt.show(block=block)
        else:
            plt.show()
        plt.close()


class NormalDistribution(Distribution):
    """Normally distributed grain-size distribution.

    A basic normally distributed grain-size distribution with defined mean and
    standard deviation. While this distribution is not really realistic, it is
    sometimes helpful. It can be readily instantiated with just two
    parameters, and so can be helpful in debugging and testing.

    .. note::

        Values less than zero are truncated, but the distribution is not
        renormalized. That is, the distributions are not *truly* truncated in
        [0,:math:`\\inf`).
    """
    def __init__(self, mean=300, sigma=80, x=None, **kwargs):
        """
        """
        scale_lim = mean + (5*sigma)
        if x:
            _x = x
        else:
            _x = np.linspace(0, scale_lim, 50)
        _dist = stats.norm(loc=mean, scale=sigma)
        _draws = _dist.rvs(size=10000)
        _vals, _ = np.histogram(_draws, bins=_x)
        _arr = (_vals / np.nansum(_vals))*100

        super().__init__(np.vstack((_x[1:], _arr)).T, **kwargs)



class LogNormalDistribution(Distribution):
    """Lognormally distributed grain-size distribution.

    .. warning::

        THIS CLASS HAS NOT BEEN IMPLEMENTED!

    """
    def __init__(self, x=None, **kwargs):
        """
        """
        raise NotImplementedError
        if x:
            _x = x
        else:
            _x = np.linspace(0, 5000, 50)
        _arr = None

        super().__init__(np.vstack((_x[1:], _arr)).T, **kwargs)



def distribution_stats():
    """Statistics of a distribution.

    mean, mode, expected value, 
    """
    raise NotImplementedError
    pass


def distribtuion_compare():
    """Statistical comparison of two distributions.

    2 sample t-test...
    """
    raise NotImplementedError
    pass
