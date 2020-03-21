import numpy as np


def velocity_roughness_z0(d90):
    """Compute roughness :math:`z0` for velocity profile.

    Computes the rougness height :math:`z_0` for the velocity profile based on the formula::

    .. math:: z_0 = k_s d_{90}


    Parameters
    ----------
    d90 : float
        The 90th percentile of the bed material grain-size distribution, given in meters.

    Returns
    -------
    float
        The roughness height :math:`z_0`.

    """
    ks = 3 * d90
    z0 = ks
    return z0


def velocity_loglaw(z, z0, ustar, alpha=1):
    """Compute velocity profile following the log-law (Law of the Wall) velocity profile.

    :cite:`Strunk1979`

    .. math::

       z0 = ks d_{90}

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

# def concentration_rouse(z, flow_depth, b, cb, Rou):
#     # nEvalPts = 51;
#     modelEvalZs = np.linspace(flow_depth*0.05, flowDepth, nEvalPts)
#     modelEvalCs = cb .* ( ((flowDepth-modelEvalZs)./modelEvalZs) ./ Hbb ) .^ Rou
#     return modelEvalZs, modelEvalCs