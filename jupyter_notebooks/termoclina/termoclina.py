"""
Script que determina la profundidad en la cual se presenta
la termoclina, a partir de datos medidos.

Gabriel Ruiz
"""

# Importando los modulos
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

# Inputs
t = np.array([22.8, 22.8, 22.8, 20.6, 13.9, 11.7, 11.1, 11.1])
z = np.array([0, 2.3, 4.9, 9.1, 13.7, 18.3, 22.9, 27.2])

# Inspeccionado los datos
# =============================================================================
# fig, ax = plt.subplots(figsize=(4,6))
# ax.plot(t, z, linestyle='None', color='r', marker='o')
# plt.xlim([0, 30])
# plt.ylim([0, 30])
# ax.xaxis.set_label_position('top')
# ax.xaxis.set_ticks_position('top')
# ax.set_ylabel('Profundidad, [m]')
# ax.set_xlabel('Temperatura, [°C]')
# ax.set_ylim(ax.get_ylim()[::-1])
# plt.show()
# =============================================================================

# Interpolando la temperatura utilizando B-splines
temp = interpolate.splrep(z, t, s=0)
zRnew = np.arange(0, 30, 0.01)
tnew = interpolate.splev(zRnew, temp, der=0)

# Calculando la primera derivada por diferencias finitas (ver Nieves)
dy = np.diff(tnew, 1)
dx = np.diff(zRnew, 1)
xprime = (1./2)*(zRnew[:-1] + zRnew[1:])
tgrad = dy/dx

# Calculando la segunda derivada
dyp = np.diff(tgrad, 1)
dxp = np.diff(xprime, 1)
tbiprime = dyp/dxp

# Conociendo el valor max absoluto de la 1era derivada que nos indica la termoclina
termo = np.abs(tgrad).max()

# Ubicando el indice donde se encuentra el valor max abs de la 1era derivada
indx = np.where(np.abs(tgrad) == termo)

# Almacenando en variable la profundidad de la termoclina
ztermo = float(zRnew[indx[0]])

# Almacenando en variable la temperatura donde se presenta la termoclina
ttermo = round(float(tnew[indx[0]])*100)/100

# Almacenando en variable el gradiente de Temperatura donde se presenta la termoclina
# y redondeando a 2 cifras sig.
tg = round(float(tgrad[indx[0]])*100)/100

# Almacenando en variable el gradiente de Temperatura donde se presenta la termoclina
# y redondeando a 2 cifras sig.
tgg = round(float(tbiprime[indx[0]])*100)/100

print('La profundidad de la termoclina es: ', ztermo, 'm')
print('La temperatura donde se presenta la termoclina es:', ttermo, '°C')
print('el gradiente de temperatura en esa profundidad es de:', tg, '°C/m')
print('y el valor de la 2da derivada donde se define la termoclina es:', tgg)

# Graficando
fig2, (ax2, ax3, ax4) = plt.subplots(1, 3, sharey=True)
ax2.plot(tnew[0:-1:100], zRnew[0:-1:100], linestyle=':', color='b', marker='+', label='Interpolacion')
ax2.plot(t, z, linestyle='None', color='k', marker='o', label='medidos')
ax2.set_ylabel('Profundidad, z, [m]')
ax2.set_ylim(ax2.get_ylim()[::-1]) 
ax2.set_xlabel('Temperatura, T, [°C]')
ax2.xaxis.set_label_position('top') 
ax2.xaxis.set_ticks_position('top') 
ax2.legend(loc=8, fontsize='x-small')

ax3.plot(tgrad[0:-1:100], zRnew[0:-1:100], linestyle='-', color='r', marker='o')
ax3.set_xlabel('dT/dz' + ' (gradiente)')
ax3.xaxis.set_label_position('top')
ax3.xaxis.set_ticks_position('top')
ax3.yaxis.set_visible(True)
#pt1, pt2 = [0, -float(zRnew[indx[0]])] , [float(tgrad[indx[0]]), -float(zRnew[indx[0]])]
#ax3.plot(pt2, pt1, linestyle=':', color='k' )

ax4.plot(tbiprime[0:-1:100], zRnew[0:-1:100], linestyle='-', color='g', marker='o')
ax4.set_xlabel(r'$dT^2/dz^2$')
ax4.xaxis.set_label_position('top')
ax4.xaxis.set_ticks_position('top')
ax4.yaxis.set_visible(True)
plt.show()

