"""Sample grain-size distributions.

There are seven grain size distributions included in this package as samples.
Each distribution is characterized by an Mx2 `ndarray`, where the first column
includes the grain size bins, and the second is a cumulative distribution.

Example
-------

Grain size samples can be instantiated as, for example::

  >>> import proffilo as pf
  >>> _yrdata = pf.sample_data.grain_size.yellow_2015()

.. note:: 
  Be sure to use ``is_cumulative=True`` if instantiating
  :class:`~proffilo.distribution.Distribution` objects with these datasets.

Available information on the grain size distributions is enumerated in the
following section.


Grain-size distributions
------------------------

:meth:`brazos` : `ndarray`
  This distribution is from the Brazos River, Texas, USA. 

:meth:`amazon` : `ndarray`
  This distribution is from the Amazon River, Brazil. 

:meth:`mississippi_SL` : `ndarray`
  This distribution is from the Mississippi River, USA. 
  It was collected near St. Louis. 

:meth:`mississippi_NO` : `ndarray`
  This distribution is from the Mississippi River, USA. 
  It was collected near New Orleans.  

:meth:`yangtze` : `ndarray`
  This distribution is from the Yangtze River, China.

:meth:`yellow_1980` : `ndarray`
  This distribution is from the Lower Yellow River, China. 
  It was collected in 1980.

:meth:`yellow_2015` : `ndarray`
  This distribution is from the Lower Yellow River, China. 
  It was collected in 2015.


Visualization
-------------

.. plot:: pyplots/sample_data/grain_size.py


"""


import numpy as np

def brazos():
  return         np.array([[135.309, 12.3625], [263.84, 28.6276], 
                           [326.862, 36.7602], [394.86, 43.9746],
                           [520.986, 53.6812], [1015.87, 63.3879], 
                           [1802.25, 70.6023], [2964.53, 78.7348],
                           [4272.12, 85.8181], [6156.44, 94.8688]])

def amazon():
  return         np.array([[53, 0.1],   [62, 0.1], 
                           [88, 0.3],   [125, 1.6], 
                           [177, 15.2], [250, 76.2], 
                           [350, 99.5], [500, 99.5], 
                           [707, 99.5], [1000, 100]])

def mississippi_SL():
  return         np.array([[125.112,2.10325], [251.189,23.9006], 
                           [499.319,57.935],  [1002.49,83.9388], 
                           [2012.72,91.9694], [8032.76,96.1759]])

def mississippi_NO():
  return         np.array([[105.561,0.172117], [153.488,1.0327], 
                           [169.869,1.89329],  [183.822,3.44234], 
                           [197.776,5.50775],  [216.582,11.1876], 
                           [236.603,18.9329],  [254.803,28.5714], 
                           [266.936,35.284],   [282.103,43.3735], 
                           [292.417,49.0534],  [312.437,58.6919],
                           [325.784,64.716],   [332.457,67.2978], 
                           [342.77,70.9122],   [353.691,74.3546], 
                           [365.217,77.4527],  [380.991,81.2392],
                           [398.584,84.6816],  [416.785,87.6076], 
                           [441.052,90.5336],  [466.532,92.599], 
                           [492.619,94.3201],  [519.919,95.6971],
                           [541.153,96.3855],  [562.386,96.9019], 
                           [593.327,97.4182],  [616.987,97.9346]])

def yangtze():
  return  np.array([[62.,0.3],    [125.,5.5], 
                    [250.,49.3],  [500.,94.8], 
                    [1000.,99.8], [2000,100]])


def yellow_1980():
  return    np.array([[5,1.8085], [10,2.8565], 
                      [25,7.9098], [50,24.1922], 
                      [100,73.9611], [250,97.3951], 
                      [500,99.832], [1000,99.9984], 
                      [2000,100]])

def yellow_2015():
  return      np.array([[0.158489,0],           [0.251189,0], 
                        [0.398107,0],           [0.630957,0.133846], 
                        [1,0.44577],            [1.584893,0.781223], 
                        [2.511886,1.190903],    [3.981072,1.551978], 
                        [6.309573,1.825797],    [10,2.602156], 
                        [15.848932,4.147535],   [25.118864,5.111823], 
                        [39.810717,7.541083],   [63.095734,23.174353], 
                        [100,57.213549],        [158.489319,88.804366],  
                        [251.188643,99.750535], [398.107171,100], 
                        [630.957344,100],       [1000,100]])
