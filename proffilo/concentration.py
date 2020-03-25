# __all__ = ['convert_mass_to_volumetric', 'convert_volumetric_to_mass']

def convert_mass_to_volumetric(mass_conc, density=2650):
    """Convert mass concentration to volumetric concentration.

    Converts a given mass concentration (e.g., g/L) to volumetric 
    concentration by assuming a constant sediment density. Formalized as:
   
    .. math::
    
        C_m = C_m / \\rho

    where :math:`C_v` is volumetric concentration, :math:`C_m` is mass
    concentration, and :math:`\\rho` is sediment density with the same units
    as :obj:`mass_conc`. For example, if :obj:`mass_conc` is given in units
    g/L, then :obj:`density` should be given in g/L.


    Parameters
    ----------

    mass_conc : float
        Mass concentration to be converted.

    density : float, optional 
        Sediment density. If not supplied, density of
        quartz is assumed (2650 g/L).


    Returns
    -------

    vol_conc : float
        Volumetric concentration.


    Examples
    --------

    >>> pf.concentration.convert_mass_to_volumetric(2, 2650)
    0.0007547169811320754

    """
    assert density > 0, 'Density must be > 0'
    assert type(density) in [float, int], 'Expected type `float` or `int`, but type was: %s' % type(density)
    vol_conc = mass_conc / density
    return vol_conc


def convert_volumetric_to_mass(vol_conc, density=2650):
    """Convert volumetric concentration to mass concentration.
    
    Converts a given volumetric concentration to mass concentration (e.g.,
    g/L) by assuming a constant sediment density. Formalized as:
    
    .. math:: 

        C_m = C_m \\times \\rho
    
    where :math:`C_m` is mass concentration, :math:`C_v` is volumetric
    concentration, and :math:`\\rho` is sediment density in desired mass
    units. For example, for mass units units g/L, :obj:`density` should be
    given in g/L.
    
    Parameters
    ----------
    
    vol_conc : float
        Volumetric concentration to be converted.

    density : float, optional 
        Sediment density. If not supplied, density of
        quartz is assumed (2650 g/L).

    Returns
    -------

    mass_conc : float
        Mass concentration in units of :obj:`density`.

    Examples
    --------

    >>> pf.concentration.convert_volumetric_to_mass(0.0003, 2650)
    0.7949999999999999

    """
    assert density > 0, 'Density must be > 0'
    assert type(density) in [float, int], 'Expected type `float` or `int`, but type was: %s' % type(density)
    mass_conc = vol_conc * density
    return mass_conc
