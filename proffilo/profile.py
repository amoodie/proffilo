import numpy as np


class BaseProfile(object):
    """Base profile class

    """
    def __init__(self):
        """
        Initialize the obj

        """
        raise NotImplementedError



class LogLawProfile(BaseProfile):
    """
    a

    """
    def __init__(self):
        """
        a

        """
        raise NotImplementedError

    def compute_velocity_loglaw(z, z0, ustar, alpha=1):
        """Compute velocity profile following the log-law (Law of the Wall) velocity profile.

        CITATIONS

        .. math::
        
            \frac{{u}}{u_*} = \frac{1}{\alpha \kappa} \ln \left( 30 \frac{z}{k_s} \right)

        Parameters
        ----------
        d90 : float
            The 90th percentile of the bed material grain-size distribution, given in meters.

        Returns
        -------
        float
            The roughness height :math:`z_0`.
            
        """
        z[z<z0] = np.nan
        vel = (ustar / (alpha * 0.41)) * np.log(z / z0);
        return vel


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
