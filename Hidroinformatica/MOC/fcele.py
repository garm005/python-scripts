# -*- coding: utf-8 -*-
def fcele(D, ethickness, Young, PoisRel, kindConduc, moduEla_K, rho):
    """
    Función que calcula la velocidad de la celeridad de la
    onda de golpe de ariete.
    
    Inputs:
    D = Diametro del conducto (m)
    ethickness = Espesor de la pared (mm)
    Young = Modulo de Elasticidad del material del conducto, Young (GPa).
    PoisRel =Relacion de Poisson (-).
    kindConduc =Tipo de Conducto
    moduEla_K = Modulo de elasticidad del fluido (GPa)
    rho = Densidaddel flujo (kg/m3)
    
    Outputs:
    a = celeridad de la onda (m/s)
    
    @author: Gabriel Ruiz
    Created on Tue Mar 14 15:09:30 2023
    Python 3.8
    """

    # Importacion del modulo
    import numpy as np
    
    RigiRock  = 0.1

    # Convirtiendo de mm a m
    ethickness = (ethickness / 1000)

    # Radio externo del conducto
    Ro = D / 2.

    # Radio interno del conducto
    ID = D - ( 2 * ethickness )
    Ri = ID / 2

    # Convirtiendo de GPA a kgf/m2
    K = moduEla_K*1E9

    # Conductos rigidos. Chaudhry ec. 2.66 p. 50
    if kindConduc == 1:
        psi = 0
        # Grueso. Conducto anclados a lo largo de su trayectoria. Chaudhry ec. 2.67 p. 51
    elif kindConduc == 2:    
        psi = 2 * (1 + PoisRel) * ( ((Ro**2 + Ri**2)/(Ro**2 - Ri**2)) - ((2 * PoisRel * Ri**2)/(Ro**2 - Ri**2)) ) 
        # Grueso. Conducto anclado en el extremo superior. Chaudhry ec. 2.68 p. 51
    elif kindConduc == 3:        
        psi = 2 * ( ((Ro**2 + (1.5 * Ri**2))/(Ro**2 - Ri**2)) + ((PoisRel *(Ro**2 - 3 * Ri**2))/(Ro**2 - Ri**2)) )    
        # Grueso. Conducto con juntas de expasion. Chaudhry ec. 2.69 p. 51
    elif kindConduc == 4:       
       psi = 2 * (((Ro**2 + Ri**2)/(Ro**2 - Ri**2)) + PoisRel)   
       # Delgado. Conducto anclado a lo largo de su trayectoria 
       # que limita el movimiento longitudinal. Chaudhry ec. 2.70 p. 52
    elif kindConduc == 5:   
        psi = (D / ethickness) * (1 - PoisRel**2)
        # Delgado. Conducto anclado en el extremo superior que 
        # evita el movimiento longitudinal. Chaudhry ec. 2.71 p. 53
    elif kindConduc == 6:   
        psi = (D / ethickness) * (1 - (0.5 * PoisRel))
        # Delgado. Conducto con juntas de expansión frecuentes. Chaudhry ec. 2.72 p. 53
    elif kindConduc == 7:   
        psi = D/ethickness
        # Tunel de roca sin revestimiento. Chaudhry ec. 2.73 p. 53
    elif kindConduc == 8:  
        psi = 1
        Young = RigiRock
        # Tunel forrado de acero. Chaudhry ec. 2.74 p. 53
    else:   
        psi = (D * Young)/((RigiRock * D) + (Young * ethickness))  

    # Calculo de celeridad de la onda
    a = np.sqrt( K /(rho * (1+((moduEla_K/Young)* psi))))
    a = np.ceil(a*100)/100

    return a
