# -*- coding: utf-8 -*-
def Qconducsen(H, Hd, L, D, epsilon, tol, hl):
    """__________________________________________________
    Funcion que calcula el gasto de un conducto sencillo.
    
    Inputs:
        H = Carga del repositorio (m)
        Hd = Carga del extremo libre (m)
        L = Longitud del conducto (m)
        epsilon = rugosidad del conducto (-)
        hl = Sumatoria de las perdidas locales (-)
        tol = tolerancia para el proceso iterativo del 
             factor de friccion.
    
    Output:
        Q1 = Gasto del conducto (m3/s)
        resul = DataFrame con los resultados de la iteracion
        
    Ejemplo:
        conducsen(85, 0, 650, 4.5, 0.015, 0.001, 1.15)
        
    Esta función requiere la subfuncion ffric, que calcula
    el factor de fricción (ffric.py).
    
    Created on Fri Feb 24 12:52:53 2023
    @author: Gabriel Ruiz
    Python 3.9
    
    """
    
    # Importando modulos y funciones
    import numpy as np
    import pandas as pd
    from ffric import ffric
	
    # ***** Constantes *****
    g = 9.81
    # __________________________________

    # Area del tubo
    A = np.pi * (D**2/4.)

    # Calculando el gasto inicial del ciclo iterativo
    Qi = A * np.sqrt((2. * g * (H - Hd))/(1. + hl))

    # Conociendo la velocidad del flujo, a partir del gasto inicial
    V1 = A / Qi

    # Calculando el factor de friccion inicial
    f1 = ffric(D, L, V1, epsilon, tol)

    # Darcy-Weisbach, Sotelo  tabla 8.3, p.293
    hf = f1 * (L/D) * (V1**2/(2. * g))

    #  Estableciendo el gasto de la iteracion siguiente
    Q1 = A * np.sqrt((2. * g * (H - Hd))/(1. + (f1*(L/D)) + hf + hl))

    tabla = np.empty([100, 3])
    tabla[0,0] = np.abs(Qi - Q1)
    tabla[0,1] = f1
    tabla[0,2] = Q1

    # Contador
    i = 1

    while np.abs(Qi - Q1) > 0.001:
        Qi = Q1
    
        V = A / Qi
        f1 = ffric(D, L, V, epsilon, tol)
        hf = f1 * (L/D) * (V**2/(2. * g))
        
        Q1 = A * np.sqrt((2. * g * (H - Hd))/(1. + (f1*(L/D)) + hf + hl))
    
        tabla[i,0] = np.abs(Qi - Q1)
        tabla[i,1] = f1
        tabla[i,2] = Q1

    i += 1

    #print('Gasto: {} m3/s'.format(np.round(Q1*100)/100))

    # Almacenando y exportando los datos en un DataFrame de Pandas
    resul = pd.DataFrame(tabla[0:i], 
                     columns=['Error', 'FriccionCoef', 'Gasto'])

    #resul.to_csv('IterSimpleC.csv', index=False, header=True)
    
    Q = np.round(Q1*100)/100
    
    return Q, resul



