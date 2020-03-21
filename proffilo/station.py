__all__ = ['Station']

import numpy as np

try:
    import matplotlib.pyplot as plt # Optional dependency
except ImportError as e:
    plt = e


from .distribution import Distribution
from . import entrain
from . import profile


class Station(object):
    """
    a
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
        self.velocity_profiles = {}


    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, var):
        self._ID = var


    @property
    def bed_distribution(self):
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
        if self._flow_depth:
            self.z = np.linspace(0, self._flow_depth, num=50)

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
    def z(self):
        return self._z

    @z.setter
    def z(self, var):
        _att_dict = self.attribute_checker(['flow_depth'])
        self._z = var


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


    def attribute_checker(self, checklist):
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


    def compute_velocity_profile(self, formula='loglaw', storestr=None, **kwargs):
        if formula in ['loglaw', 'lotw', 'lawofthewall']:
            _att_dict = self.attribute_checker(['flow_depth', 'z', 'ustar'])
            _z0 = profile.velocity_roughness_z0(self.bed_distribution.d(90, units='microns')*1e-6) # hardcoded for microns!
            _vel = profile.velocity_loglaw(self.z, _z0, self.ustar, alpha=1)
            if not storestr:
                storestr = 'loglaw'
        else:
            raise ValueError('Invalid velocity formula provided: %s.' % formula)

        self.velocity_profiles[storestr] = [_vel, kwargs]


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
        """
        Show the distribution
        """
        self._mpl_check()

        xlab = kwargs.pop('xlabel', 'velocity ('+'m/s'+')')
        ylab = kwargs.pop('ylabel', 'depth ('+'m'+')')
        
        fig, ax = plt.subplots()
        for v, prof in enumerate(self.velocity_profiles):
            _prof = self.velocity_profiles[prof]
            ax.plot(_prof[0], self.z, **_prof[1])    
        
        ax.legend(self.velocity_profiles.keys())
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        if savestr:
            fig.savefig(savestr)
            plt.show(block=block)
        else:
            plt.show()
