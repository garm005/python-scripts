# -*- coding: utf-8 -*-
"""
Script que importa los datos de un archivo mat (Sontek Surveyor M9) a
Python.

Created on Mon Jul 31 13:35:43 2023
@author: Gabriel
"""

import scipy.io as sio
import numpy as np
import pandas as pd

def obj_array_to_type(arr, typ):
    """
    Convert an object array of same-sized arrays to a normal 3D array
    with dtype=typ. This is a workaround as numpy doesn't realize that
    the object arrays are numpy arrays of the same legth, so just using
    array.astype(typ) fails. Technically works if the items are numbers
    and not arrays, but then `arr.astype(typ)` should be used.
    """
    full_shape = (*arr.shape, *np.shape(arr.flat[0]))
    return np.vstack(arr.flatten()).astype(typ).reshape(full_shape)

datos = sio.loadmat('20230719091839', appendmat=True, struct_as_record=True,
                    squeeze_me=True)

dBT = datos["BottomTrack"]["BT_Depth"]
dBT1d = dBT.flatten()
dBT1d = np.vstack(dBT1d)
dBT = dBT1d.reshape(dBT1d.size)
del dBT1d

dvb = datos["BottomTrack"]["VB_Depth"]
dVb = np.vstack(dvb.flatten())
dVB = dVb.reshape(dVb.size)
del dvb, dVb

longi = datos["GPS"]["Longitude"]
longit = np.vstack(longi.flatten())
lon = longit.reshape(longit.size)
del longi, longit

latid = datos["GPS"]["Latitude"]
lati = np.vstack(latid.flatten())
lat = lati.reshape(lati.size)
del latid, lati

utmd = datos["GPS"]["UTM"]
utm1 = np.stack(utmd.flatten())
utm = utm1.reshape(utm1.size)
del utmd, utm1

yind = np.where(utm > 1000000)
y = utm[yind]
xind = np.where(utm < 600000)
x = utm[xind]
del yind, xind

data = pd.DataFrame({'lon(°)':lon, 'lat(°)':lat, 'x(m)':x, 
                     'y(m)':y, 'BT(m)':dBT, 'VB(m)':dVB})
print(data.head())

data.to_csv('datos.csv', header=False, index=False)