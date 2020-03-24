import sys, os
sys.path.append(os.path.realpath(os.getcwd()+"/../.."))

import matplotlib.pyplot as plt

from proffilo.distribution import Distribution
from proffilo.sample_data import grain_size as gs

_brazos = Distribution(arr=gs.brazos(), is_cumulative=True)
_amazon = Distribution(arr=gs.amazon(), is_cumulative=True)
_mississippi_SL = Distribution(arr=gs.mississippi_SL(), is_cumulative=True)
_mississippi_NO = Distribution(arr=gs.mississippi_NO(), is_cumulative=True)
_yangtze = Distribution(arr=gs.yangtze(), is_cumulative=True)
_yellow_1980 = Distribution(arr=gs.yellow_1980(), is_cumulative=True)
_yellow_2015 = Distribution(arr=gs.yellow_2015(), is_cumulative=True)

dist_list = [_brazos, _amazon, _mississippi_SL, _mississippi_NO, _yangtze, _yellow_1980, _yellow_2015]

fig, ax = plt.subplots()
for d, dist in enumerate(dist_list):
    plt.plot(dist.bin, dist.cumulative_dist)
ax.set_xscale('log')
ax.set_ylim((0,100))
ax.set_ylabel('percent finer (%)')
ax.set_xlabel('grain size '+r'$(\mu m)$')
ax.legend(['brazos', 'amazon', 'mississippi_SL', 'mississippi_NO', 'yangtze', 'yellow_1980', 'yellow_2015'])
plt.show()
