__all__ = ['BaseProfile', 'LogLawProfile', 'RouseProfile']

import numpy as np
import abc
from .velocity import compute_velocity_loglaw


class BaseProfile(object):
    """Base profile class.

    .. note::

        This class should **never** be instantiated directly.

    Attributes
    ----------

    z : `ndarray`
        Vertical coordinate vector.

    z_norm : `ndarray`
        Normalized vertical coordinate vector.

    """
    def __init__(self, flow_depth, z0=0, nz=50):
        """
        Initialize the Profile.

        """
        self.flow_depth = flow_depth
        self.z = np.linspace(z0, self.flow_depth, num=nz)

    @property
    def z(self):
        """
        Vertical coordinate vector.
        """
        return self._z

    @property
    def z_norm(self):
        """Normalized vertical coordinate vector. 

        Values are normalized into the interval [0,1], by dividing `z` by the
        `flow_depth`.
        """
        return self._z_norm

    @z.setter
    def z(self, var):
        self._z = var
        _norm = var / self.flow_depth
        assert _norm[0] >= 0 and _norm[-1] <= 1
        self._z_norm = _norm

    @property
    @abc.abstractmethod
    def val(self):
        """
        Value of profile vector.
        """
        return self._val

    @val.setter
    def val(self, var):
        self._val = var

    @abc.abstractmethod
    def compute_values(self):
        """Compute values of the profile. 

        Must be reimplemented by subclasses.
        """
        pass


class LogLawProfile(BaseProfile):
    """Log-law velocity profile model
    
    Log-law velocity profile model, defined by::

    .. math:: \\frac{u}{u_*} = \\frac{1}{\\alpha \\kappa} \\ln \\left( 30 \\frac{z}{k_s} \\right)

    Also known as the Law-of-the-wall.
    """
    def __init__(self, flow_depth, z0, ustar, alpha=1, nz=50):
        """
        a

        """
        super().__init__(flow_depth, z0, nz=nz)

        self.type = 'velocity'
        self.z0 = z0
        self.ustar = ustar
        self.alpha = alpha

        self.velocity = self.compute_values()


    def compute_values(self):
        """Compute velocity profile.

        Alias to :doc:`proffilo.velocity.compute_velocity_loglaw`.
        """
        _velocity = compute_velocity_loglaw(self.z, self.z0, self.ustar, alpha=self.alpha)
        print(self.z)
        return _velocity




class RouseProfile(BaseProfile):
    """Docstring

    The Rouse formula is given by::

    .. math::

        \\frac{{c}_i}{{c}_{bi}} = \\left[ \\frac{(H-z)/z}{(H-b)/b} \\right] ^{Z_{Ri}}
        
    And the Rouse number, given by::

    .. math::
    
        Z_{Ri} = \\frac{w_{si}}{\\alpha \\kappa u_*}
    
    Attributes
    ----------

    Another strng.
    
    """
    def __init__(self):
        raise NotImplementedError
        pass

    def concentration_rouse(z, flow_depth, b, cb, Rou):
        # nEvalPts = 51;
        # modelEvalZs = np.linspace(flow_depth*0.05, flowDepth, nEvalPts)
        # modelEvalCs = cb .* ( ((flowDepth-modelEvalZs)./modelEvalZs) ./ Hbb ) .^ Rou
        # return modelEvalZs, modelEvalCs
        pass
