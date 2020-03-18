import numpy as np 

try:
    import matplotlib.pyplot as plt # Optional dependency
except ImportError as e:
    plt = e


class Distribution(object):
    """
    """
    def __init__(self, arr, units='microns'):
        self.data = arr
        self.bin = self.data[:,0]
        self.dist = self.data[:,1]
        self.cumulative_dist = np.cumsum(self._dist)
        self.units = units


    @property
    def data(self):
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
        if self._units in ['microns', 'micron', 'mum', '\mum', 'mu m']:
            self.display_units = '$\mu$m'
        elif self._units in ['phi', '\phi']:
            self.display_units = '$\phi$'


    @property
    def cumulative_dist(self):
        return self._cumulative_dist

    @cumulative_dist.setter
    def cumulative_dist(self, var):
        self._cumulative_dist = var


    def __repr__(self):
        return str(self.data)

        
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
