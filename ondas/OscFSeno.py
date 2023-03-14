# -*- coding: utf-8 -*-
"""
Script que grafica la oscilación entre 1 y -1 de la función seno
Created on Tue Oct 18 13:00:50 2022
@author: Gabriel Ruiz
"""

# Importación de los modulos

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines

# Inputs

A = 1.0

# Estableciendo el arreglo con los valores de los angulos que se graficarán.

theta = np.arange(0, 360+1, 10)*np.pi/180.



# Coordenadas del circulo que usaremos para ver la oscilación del ángulo.
a = A * np.cos(theta)
b = A * np.sin(theta)

# ## Graficacion
# Para usar LaTeX en las graficas.

plt.rcParams['text.usetex']='True'

# Específicando el estilo de graficación.

plt.style.use('seaborn-notebook')

# Abriendo la figura.

fig, (ax1, ax2) = plt.subplots(1,2, figsize=[9, 6])

# Vamos a editar las características de los ejes donde vamos a graficar la función seno.

ax2.set_ylim((-1, 1))
ax2.plot(theta, np.zeros((len(theta), 1)), color='k', linestyle='-', \
            linewidth=0.5)
ax2.set_ylabel('Amplitud')
ax2.set_xlabel(r'$\theta$'+' (°)')
ax2.set_xlim((theta[0], theta[-1]))
ax2.set_xticks([0, 2, 4, 6])
ax2.set_xticklabels(['0', '120', '230', '350'])

# Vamos a graficar la función seno para cada ángulo que se estableció.

# +

for i in range(len(theta)):
    print('Graficando el angulo: {0:5f}'.format(theta[i]))
    
    # Borrando el eje 1.
    ax1.cla()
    
    # Dibujando el circulo de radio A.
    ax1.plot(a, b, color='g')
    ax1.set_aspect('equal')
    ax1.axis('off')

    # Dibujando las lineas de los cuadrantes.
    ax1.add_artist(lines.Line2D([0, 0], [-1, 1], color='gray', \
                   linewidth=1))
    ax1.add_artist(lines.Line2D([-1, 1], [0, 0], color='gray', \
                   linewidth=1))
    
    # Dibujando la línea y el punto que se mueven.
    ax1.plot(a[i], b[i], marker='o', color='red')
    ax1.plot([0, a[i]], [0, b[i]], color='purple')
    ax1.annotate(r'$\theta = $'+str(theta[i]*(180./np.pi))+'°', \
                 xy=(0.78, 0.78), xycoords='data', fontsize=10)

    # Dibujando los puntos en el plano cartesiano.
    ax2.plot(theta[i], b[i], marker='o', color='red')

    # Importando la figura hacia un archivo.
    plt.savefig('funcionSeno0'+str(i)+'.png')

    plt.draw()
