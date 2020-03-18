import numpy as np

from .distribution import Distribution
from . import entrain


class Station(object):
    """
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
        # self.velocity_profiles = []

        # self.set_z()
        # self._z = 50


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
        self._flow_depth = var
        if self.flow_depth:
            self._z = 50


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

    @property
    def _z(self):
        return self._z

    @_z.setter
    def _z(self, nz=50):
        _att_dict = self.attribute_checker(['flow_depth'])
        self._z = np.linspace(0, self.flow_depth, nz)


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

    def compute_velocity_profile(self, formula='loglaw'):
        pass


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
