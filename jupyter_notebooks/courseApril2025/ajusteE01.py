# -*- coding: utf-8 -*-
"""
Este script resuelve los problemas del 3.1 al 3.4 del libro
Campos, D.F. 2005. Introducción a la Hidrología Urbana. Mex. 307 p.

El archivo de datos debera de tener una extensión *.csv y solo debe de
tener 3 columnas sin encabezados
    1era columna. Fecha
    2da. columna. Gasto en m3/s
    3ra. columna. Volumen en m3
    
El flag1= 1 indica que los datos se van a estandarizar; cuando esta opcion
   se elija, el valor del area del cuerpo de agua debe proporcionarse

@author: Gabriel Ruiz Martinez
"""

# Importando los modulos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Proporcionando el nombre del archivo con los datos
namefile = 'qmaxanualMadin.csv'
# Estableciendo el flag que indica si los datos se encuentran estandarizados
flag01 = 1  # 1 = Estan estandarizados los datos, 0 = no estandarizados.

# Cargando los datos
datos = pd.read_csv(namefile, sep=',', header=None,
                    names=['years', 'Gasto (m3/s)', 'Vol (m3)'])