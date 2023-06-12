import allantools
import numpy as np
y=np.loadtxt("noisetest.ykt", encoding="latin1",comments='%')
t = np.logspace(0, 4, 15)  # tau values from 1 to 10000
(t2, ad, ade, adn) = allantools.ohdev(y[:,1], rate=1, data_type="freq", taus=t) # overlapping HDEV
print(t2)
print(ad)
(t2, ad, ade, adn) = allantools.oadev(y[:,1], rate=1, data_type="freq", taus=t) # overlapping ADEV
print(t2)
print(ad)
