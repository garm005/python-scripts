# -*- coding: utf-8 -*-
"""
Script que grafica un diagrama TS a partir de un lance
de CTD.

Como resultado se exportan la graficas hacia archivos *.png

@author: Gabriel Ruiz
"""

# importando los modulos
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import gsw
import simplekml

# Cargando los datos de un archivo mat
inputfile = 'CC1739001_20211019_143447.mat'
datos = sio.loadmat(inputfile)

# Clasificando las variables de interes 
temp = datos['Temperature']
sali = datos['Salinity']
z = datos['Depth']
lat = datos['LatitudeStart']
lon = datos['LongitudeStart']

# Para establecer los rangos en los cuales vamos a graficar los valores de T y S, calculemos los valores
# máximos y mínimos de cada párametro
prescS = 1./100
prescT = 1./10

smin = sali.min() - (prescS * sali.min())
smax = sali.max() + (prescS * sali.max())

tmin = temp.min() - (prescT * temp.max())
tmax = temp.max() + (prescT * temp.max())
 
# Obteniendo el número de nodos que requieren para representar el rango de cada parámetro:
snodes = int(round((smax-smin)/0.1 + 1, 0))
tnodes = int(round((tmax-tmin) + 1, 0))
 
# Dimensionando la matriz donde se calculara la densidad
rhoabs = np.zeros((tnodes, snodes))
 
# Estableciendo los vectores para cada eje
tem = np.linspace(1, tnodes-1 ,tnodes) + tmin
sal = np.linspace(1, snodes-1, snodes)*0.1 + smin
 
# Calculando la densidad a partir de la salinidad, temperatura y la presion
# en este caso la presion es 0
for j in range(0, int(tnodes)):
    for i in range(0, int(snodes)):
        rhoabs[j, i] = gsw.rho(sal[i], tem[j], 0)
  
# Obteniendo el parametro sigma-t
rhoabs = rhoabs - 1000
 
# Graficando
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
hc = plt.contour(sal, tem, rhoabs, linestyles=':', colors='b')
plt.clabel(hc, fontsize=10, inline=1, fmt='%1.2f')
ax1.plot(sali, temp, 'or', linestyle='None', marker='o', color='r', markersize=9, markeredgecolor='k')
ax1.set_xlabel('Salinidad, [uS]')
ax1.set_ylabel('Temperatura, [°C]')
#plt.show()
plt.savefig('diaTS.png')

_, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(temp, z, '-r', marker='h', markerfacecolor='red', markeredgecolor='k')
ax1.set_ylim(ax1.get_ylim()[::-1])
ax1.set_ylabel('Profundidad, [m]')
ax1.set_xlabel('Temperatura, [°C]')
ax1.xaxis.set_label_position('top')
ax1.xaxis.set_ticks_position('top')
ax2.plot(sali, z, '-b', marker='h', markerfacecolor='blue', markeredgecolor='k')
ax2.set_xlabel('Salinidad, [uS]')
ax2.xaxis.set_label_position('top')
ax2.xaxis.set_ticks_position('top')
ax2.yaxis.set_visible(False)
plt.show()
#plt.savefig('TvDSvD.png')

print('\nExportando los nodos a un archivo *.kml de Google Earth...')
kmlfile = simplekml.Kml()
kmlfile.newpoint(name='PuntoCTD', coords=[(float(lon), float(lat))])
kmlfile.save('PuntoCTD.kml')

