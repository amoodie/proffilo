import sys, os
sys.path.append(os.path.realpath(os.getcwd()+"/../.."))

import matplotlib.pyplot as plt

from proffilo.profile import LogLawProfile
import proffilo.velocity as velocity

fd = 5                              # flow depth
z0 = velocity.compute_roughness_z0(300e-6)   # roughness height
us = 0.05                           # shear velocity
ll_prof = LogLawProfile(fd, z0, us)
ll_prof.show_profile()
