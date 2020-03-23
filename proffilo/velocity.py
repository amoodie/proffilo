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
        """Compute velocity profile following the log-law (Law of the Wall) velocity profile.

        CITATIONS

        .. math::
        
            \frac{{u}}{u_*} = \frac{1}{\alpha \kappa} \ln \left( 30 \frac{z}{k_s} \right)

        Parameters
        ----------
        
        Returns
        -------
        
            
        """
        z[z<z0] = np.nan
        vel = (ustar / (alpha * 0.41)) * np.log(z / z0);
        return vel