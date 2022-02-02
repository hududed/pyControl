# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 13:37:38 2022

@author: UWAdmin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 18:59:03 2022

@author: UWAdmin
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:11:19 2021

@author: UWAdmin
"""

import LRPC


#%%

#laser = LRPC.LaserSystemControl()
#raman = LRPC.RamanSpectrometerControl()
#cell = LRPC.CellAndMirrorControl()

sc = LRPC.SystemControl()

sc.set_laser_power(0.01)

#sc.power_off_laser()
#%%