# -*- coding: utf-8 -*-
"""
Método de la bisección.
En la funcion fdeX se debe proporcionar la funcion a
la cual se desea encontrar su raiz o solucion.

Algoritmo 2.1 de Burden, R. y Faires, J. 1993.
Analisis Numerico


@author: Gabriel Ruiz Martinez
"""

import numpy as np
import math
import matplotlib.pyplot as plt

def fdeX(x):
    '''
    En esta funcion se debera proporcionar
    la ecuacion de una variable que se desea
    encontrar su raiz.
    
    Inputs:
    x, valor de la variable independiente
    
    Output:
    el valor de la funcion evaluada en el valor de la
    variable independiente
    '''
    
    return x**3 + 4*x**2 - 10

def biseccion(a, b, tol=1E-3):
    '''
    Funcion que encuentra la raiz de una ecuacion
    de una variable. El metodo de biseccion se
    usa para encontrar la raiz.

    Inputs:
    a, Valor de extremo izquierdo donde se buscara
        la raiz. Tipo float
    b, Valor de extremo derecho donde se buscara la
        raiz. Tipo float
    tol, Valor de la tolerancia. Su valor por default es
        1E-10. Este parametro es opcional

    Output:
    p, Valor de la raiz. Tipo float
    '''
    
    i = 1
    fa = fdeX(a)
    
    No = int(np.ceil((np.log(b-a) - np.log(tol))/np.log(2)))
    
    while i <= No:
        p = a + (b-a)/2
        fp = fdeX(p)
        if fp == 0 or (b-a)/2 < tol:
            # print('La raiz es: ', p)
            # print('Iteracion:', i)
            # print('a = ', a)
            # print('b = ', b)
            break
        i += 1
        if np.sign(fa)*np.sign(fp) > 0:
            a = p
        else:
            b = p
    return p

vi = 1.0
vf = 2.0
r = biseccion(vi, vf, 1E-3)
print(r)  

x = np.arange(vi, vf, 0.1)
plt.plot(x, fdeX(x))
plt.show()
