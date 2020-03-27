import numpy as np


def compute_roughness_z0(d90):
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


def compute_velocity_loglaw(z, z0, ustar, alpha=1):
    """Compute log-law velocity profile.

    Compute a velocity profile following the log-law (a.k.a. Law of the
    Wall) formualtion. Takes as input the vector of vertical coordinates
    `z`, the roughness height `z0`, the shear velocity `ustar`, and
    optionally the stratification adjustment coefficient :math:`\\alpha`.

    CITATIONS

    .. math:: \\frac{u}{u_*} = \\frac{1}{\\alpha \\kappa} \\ln \\left( 30 \\frac{z}{k_s} \\right)

    Parameters
    ----------
    z : `ndarray`
        Vertical coordinate vector.

    z0 : `float`
        Roughness height.

    ustar : `float`
        Shear velocity.

    alpha : `float`
        Stratification adjustment coefficient.
    
    Returns
    -------
    velocity : `ndarray`
        Velocity estimated at `z`
        
    """
    z[z<=z0] = np.nan
    velocity = (ustar / (alpha * 0.41)) * np.log(z / z0);
    return velocity