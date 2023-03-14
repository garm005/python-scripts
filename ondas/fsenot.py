# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 10:21:32 2022

@author: Gabriel
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 10:04:36 2022

@author: Gabriel
"""

import numpy as np
import matplotlib.pyplot as plt

# Inputs
A = 1.0


# Determinacion de los angulos
seg = np.arange(0, 59+1, 0.1)
minu = np.arange(0, 60, 0.1)
hora = np.arange(0, 11+1, 0.1)
#thetarad = theta*(np.pi/180.)

# Calculo de la funcion seno
sen = A * np.sin(seg)
sen_m = A * np.sin(minu)
sen_h = A * np.sin(hora)

# Graficacion
# Para usar LaTeX en las graficas
plt.rcParams['text.usetex'] = False

# Especificando el estilo de graficación
plt.style.use('seaborn-notebook')

fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize= [6.4, 12])
ax1.plot(seg, sen, color='r', linewidth=1)
#ax.plot(minu, sen_m, color='b',linewidth=2)
#ax.plot(hora, sen_h, color='g',linewidth=3)
ax1.plot(seg, np.zeros((len(seg), 1)), color='k', linestyle='-', \
        linewidth=0.5)
ax1.set_xlabel('Tiempo (s), 60s = 1 minuto')
ax1.set_ylabel('Amplitud')
ax1.set_xlim((seg[0], seg[-1]))

ax2.plot(minu, sen_m, color='b', linewidth=2)
#ax.plot(hora, sen_h, color='g',linewidth=3)
ax2.plot(minu, np.zeros((len(minu), 1)), color='k', linestyle='-', \
        linewidth=0.5)
ax2.set_xlabel('Tiempo (min), 60min = 1 minuto')
ax2.set_ylabel('Amplitud')
ax2.set_xlim((minu[0], minu[-1]))

ax3.plot(hora, sen_h, color='g',linewidth=3)
ax3.plot(hora, np.zeros((len(hora), 1)), color='k', linestyle='-', \
        linewidth=0.5)
ax3.set_xlabel('Tiempo (hr)')
ax3.set_ylabel('Amplitud')
ax3.set_xlim((hora[0], hora[-1]))
#plt.savefig('funcionSeno.png')
plt.draw()