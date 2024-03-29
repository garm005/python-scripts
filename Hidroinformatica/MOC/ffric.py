# -*- coding: utf-8 -*-
def ffric(D, L, V, epsilon, tol):
    """
    Calculo del factor de friccion, usando el metodo iterativo simple de punto fijo.
    
    Inputs:
    D = diametro de la tuberia (m),
    L = longitud de la tuberia (m) ,
    V = velocidad del flujo en la tuberia (m/s),
    tol = tolerancia (-).
    
    Output:
    cf = coeficiente de friccion (-)

    @author: Gabriel Ruiz Martinez
    Created on Thu Feb  9 11:53:48 2023
    Python 3.8
    """
    # Importando modulos
    import numpy as np

    # Aceleracion de la gravedad (m2/s)
    g = 9.81
    
    # Viscosidad cinematica para agua a 20°C
    nu = 1.0E-6

    # Calculando el numero de Reynolds (Fzas. inerciales / Fzas. viscosas)
    Re = (V * D) / nu
    
    # Calculo de la rugosidad relativa
    erel = epsilon / D

    # Determinando el tipo de flujo
    if Re == 0:
        f1 = 0
    elif Re < 2300:         # Tubos lisos o rugosos en zona laminar
        f1 = 64./Re                # Poiseuille, Sotelo ec. 8.3 p.279
    else:
        flprandtl = epsilon/(3.7 * D)      # Usando la ecuacion de Nikuradse, Potter ec. 7.6.27 p. 307
        C = flprandtl
        ld = -0.86 * np.log(C)
        f1 = (1./ld)**2

        flkarman = 2.51/(Re * np.sqrt(f1))   # Usando la ec. de Colebrook-White, Potter ec. 7.6.28 p. 307
        C = flprandtl + flkarman
        ld = -0.86 * np.log(C)
        f2 = (1./ld)**2

        #if np.abs(f1 - f2) > tol:
        while np.abs(f1 - f2) > tol:
             f1 = f2
             f2 = 0
             flkarman = 2.51/(Re * np.sqrt(f1))
             C = flprandtl + flkarman
             ld = -0.86 * np.log(C)
             f2 = (1./ld)**2
        f1 = f2
    
    cf = np.round(f1 * 1E6)/1E6
    
    return cf
