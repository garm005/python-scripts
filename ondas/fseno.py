# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 10:04:36 2022

@author: Gabriel
"""

import numpy as np
import matplotlib.pyplot as plt

# Inputs
A = 1.0
intang = 360

# Determinacion de los angulos
theta = np.arange(0, intang+1, 10)
thetarad = theta*(np.pi/180.)

# Calculo de la funcion seno
sen = A * np.sin(thetarad)

# Impresión de los resultados
print('i\t\tTheta\t\t\tAngulo(rad)\t\t\tAmplitud')
for i in range(len(theta)):
    print('{0:4d}\t\t{1:4d}\t\t{2:6f}\t\t {3:6f}'.format(i, theta[i], \
            thetarad[i], sen[i]))

# Graficacion
# Para usar LaTeX en las graficas
plt.rcParams['text.usetex'] = False

# Especificando el estilo de graficación
plt.style.use('seaborn-notebook')

fig, ax = plt.subplots()
ax.plot(thetarad, sen, color='r', linewidth=3)
ax.plot(thetarad, np.zeros((len(theta), 1)), color='k', linestyle='-', \
        linewidth=0.5)
ax.set_xlabel('Angulo (rad)')
ax.set_ylabel('Amplitud')
ax.set_xlim((thetarad[0], thetarad[-1]))
plt.savefig('funcionSeno.png')
plt.draw()