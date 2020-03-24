__all__ = ['Station']

import numpy as np

try:
    import matplotlib.pyplot as plt # Optional dependency
except ImportError as e:
    plt = e


from .distribution import Distribution
from . import entrain
from . import profile
from . import velocity
from . import concentration


class Station(object):
    """Survey station entity.

    Survey station class. Provides organization to other objects that are
    related to the survey station. Many object can be initialized from
    `Station` methods, or by assignment (see examples below). Additionally
    provides a number of helpful plotting and visualization functions.

    Attributes
    ----------
    ID : `str`
        Identification string for the survey station, should be a unique identifier.
    
    bed_distribution : :obj:`proffilo.distribution.Distribution`
        Grain size distribution for bed material.
    
    flow_depth : `float`
        Flow depth at the station [m].
    
    ustar : `float`
        Shear velocity [m/s].

    slope : `float`
        Water surface slope [-].

    nearbed_concentration : `float`
        Shear velocity [m/s]

    Methods
    -------

    See Also
    --------

    Examples
    --------
    >>> stn = pf.Station(ID='YR0094')
    
    """
    def __init__(self, ID, bed_distribution=None, flow_depth=None, ustar=None, 
                 slope=None, 
                 nearbed_distribution=None, nearbed_concentration=None):

        self.ID = ID
        self.bed_distribution = bed_distribution
        self.flow_depth = flow_depth
        self.ustar = ustar
        self.slope = slope
        self.nearbed_concentration = nearbed_concentration
        self._velocity_profiles = {}


    @property
    def ID(self):
        """
        Identification string, should be unique to the station.
        """
        return self._ID

    @ID.setter
    def ID(self, var):
        self._ID = var


    @property
    def bed_distribution(self):
        """
        Properties created with the ``@property`` decorator should be documented
        in the property's getter method.
        """
        return self._bed_distribution

    @bed_distribution.setter
    def bed_distribution(self, var):
        if type(var) is Distribution:
            self._bed_distribution = var
        else:
            self._bed_distribution = None


    @property
    def flow_depth(self):
        return self._flow_depth

    @flow_depth.setter
    def flow_depth(self, var):
        _var, _units = self._unit_stripper(var)
        self._flow_depth = _var
        # self._flow_depth_units = _units

    # @property
    # def flow_depth_units(self):
    #     return self._flow_depth_units

    # @flow_depth_units.setter
    # def flow_depth_units(self, var, default='meters'):
    #     if var:
    #        self._flow_depth_units = var
    #     else:
    #         self._flow_depth_units = default


    @property
    def ustar(self):
        return self._ustar

    @ustar.setter
    def ustar(self, var):
        self._ustar = var


    @property
    def slope(self):
        return self._slope

    @slope.setter
    def slope(self, var):
        self._slope = var


    @property
    def nearbed_concentration(self):
        return self._nearbed_concentration

    @nearbed_concentration.setter
    def nearbed_concentration(self, var):
        if var is not None:
            assert var.ndim == 1
            assert len(var) == len(self._bed_distribution.bin)
            self._nearbed_concentration = var
        else:
            self._nearbed_concentration = None


    def _unit_stripper(self, var):
        if type(var) is list:
            return var[0], var[1]
        else:
            return var, None


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
            raise RuntimeError('Required attribute(s) not assigned: '+str(log_form))
        return att_dict


    def add_velocity_profile(self, formula='loglaw', storestr=None, nz=50, **kwargs):
        if formula in ['loglaw', 'lotw', 'lawofthewall']:
            _alpha = kwargs.pop('alpha', 1.0)
            _att_dict = self._attribute_checker(['flow_depth', 'ustar'])
            _z0 = velocity.compute_roughness_z0(self.bed_distribution.d(90, units='microns')*1e-6) # hardcoded for microns!
            _prof = profile.LogLawProfile(flow_depth=self.flow_depth, z0=_z0, 
                                         ustar=self.ustar, alpha=_alpha, nz=nz)
            if not storestr:
                storestr = 'loglaw'
        else:
            raise ValueError('Invalid velocity formula provided: %s.' % formula)

        self._velocity_profiles[storestr] = [_prof, kwargs]


    def compute_entrainment_from_bed(self, formula='wright_parker', replace=False):
        """
        if replace is true, put it into the nearbed slot, 
        otherwise put it into a new predicted slot only
        """
        raise NotImplementedError()
        # do all kinds of general checks, bare minimum is bed gsd
        if formula in ['wright_parker', 'wright_parker_2004', 'wright_parker_04', 'WP04']:
            entrain.wright_parker()
        else:
            raise ValueError('Invalid entrainment formula provided: %s.' % formula)


    def _mpl_check(self):
        if isinstance(plt, ImportError):
            raise plt

    def show_velocity(self, block=False, savestr=None, **kwargs):
        """Plot velocity profiles.

        Plot the velocity profiles.
        """
        self._mpl_check()
        assert len(self._velocity_profiles) > 0, 'No velocity profiles found.'

        xlab = kwargs.pop('xlabel', 'velocity ('+'m/s'+')')
        ylab = kwargs.pop('ylabel', 'depth ('+'m'+')')
        
        fig, ax = plt.subplots()
        for v, prof in enumerate(self._velocity_profiles):
            _prof, _mplkwargs = self._velocity_profiles[prof]
            ax.plot(_prof.velocity, _prof.z, **_mplkwargs)    
        
        ax.legend(self._velocity_profiles.keys())
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        if savestr:
            fig.savefig(savestr)
            plt.show(block=block)
        else:
            plt.show()
