__all__ = ['BaseProfile', 'LogLawProfile', 'RouseProfile']

import numpy as np
import abc
from .velocity import compute_velocity_loglaw

try:
    import matplotlib.pyplot as plt # Optional dependency
except ImportError as e:
    plt = e


class BaseProfile(object):
    """Base profile class.

    .. warning::

        This class should **never** be instantiated directly.

    """
    def __init__(self, flow_depth, z0=0, nz=50):
        """
        Initialize the Profile.

        """
        self.flow_depth = flow_depth
        self.z = np.linspace(z0, self.flow_depth, num=nz)

    @property
    def z(self):
        """`ndarray` : Vertical coordinate vector.

        Vertical coordinate vector [m].
        """
        return self._z

    @property
    def z_norm(self):
        """`ndarray` : Normalized vertical coordinate vector. 

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

    def _mpl_check(self):
        if isinstance(plt, ImportError):
            raise plt

    def show_profile(self, block=False, savestr=None, **kwargs):
        """Show the profile.
        
        Show the profile in a plot. 

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

        xlab = kwargs.pop('xlabel', self.type+' ('+self.display_units+')')
        ylab = kwargs.pop('ylabel', 'distance above bed (m)')
        
        fig, ax = plt.subplots()
        ax.plot(self.val, self.z, **kwargs)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        if savestr:
            fig.savefig(savestr)
            plt.show(block=block)
        else:
            plt.show()



class LogLawProfile(BaseProfile):
    """Log-law velocity profile model
    
    Log-law velocity profile model, defined by

    .. math:: 
        \\frac{u}{u_*} = \\frac{1}{\\alpha \\kappa} \\ln \\left( 30 \\frac{z}{k_s} \\right)

    Also known as the Law-of-the-wall.

    Examples
    --------

    Initialize a log-law model profile.
        >>> from proffilo.profile import LogLawProfile
        >>> import proffilo.velocity
        >>> fd = 5                                           # flow depth
        >>> z0 = ks = velocity.compute_roughness_z0(300e-6)  # roughness height
        >>> ustar = 0.05                                     # shear velocity
        >>> ll_prof = LogLawProfile(fd, z0, ustar)

    Visualize the profile.
        >>> ll_prof.show_profile()

    .. plot:: pyplots/profile/loglawprofile.py

    """
    def __init__(self, flow_depth, z0, ustar, alpha=1, nz=50):
        """Initialize a LogLawProfile.
        
        Calls :func:`~proffilo.profile.LogLawProfile.compute_values` once.

        Parameters
        ----------
        flow depth : `float`
            Flow depth [m].

        z0 : `float`
            Roughness height [m].

        ustar : `float`
            Shear velocity [m/s].

        alpha : `float`, optional
            Stratification coefficient, default is 1.0 [-].

        nz : `int`, optional
            Number of discrete vertical coordinates in ``z``, default is 50.

        """
        super().__init__(flow_depth, z0, nz=nz)

        self.type = 'velocity'
        self.z0 = z0
        self.ustar = ustar
        self.alpha = alpha
        self.display_units = 'm/s'

        self.velocity = self.compute_values()

    @property
    def z0(self):
        """`float` : Roughness height [m].
        """
        return self._z0

    @z0.setter
    def z0(self, var):
        self._z0 = var

    @property
    def flow_depth(self):
        """`float` : Flow depth [m].
        """
        return self._flow_depth

    @flow_depth.setter
    def flow_depth(self, var):
        self._flow_depth = var

    @property
    def ustar(self):
        """`float` : Shear velocity [m/s].
        """
        return self._ustar

    @ustar.setter
    def ustar(self, var):
        self._ustar = var

    @property
    def alpha(self):
        """Stratification adjustment coefficient [-].
        """
        return self._alpha

    @alpha.setter
    def alpha(self, var):
        self._alpha = var

    @property
    def velocity(self):
        """Velocity values.

        Profile velocity values along the ``z`` coordinate.
        """
        return self._velocity

    @velocity.setter
    def velocity(self, var):
        self._velocity = var
        self._val = self._velocity


    def compute_values(self):
        """Compute velocity profile.

        Compute the velocity profile from ``self`` attributes. This method is
        called once during :func:`~proffilo.profile.LogLawProfile.__init__`, but can be called to recompute values, as
        needed. 

        Alias to :doc:`proffilo.velocity.compute_velocity_loglaw`.
        """
        _velocity = compute_velocity_loglaw(self.z, self.z0, self.ustar, alpha=self.alpha)
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
