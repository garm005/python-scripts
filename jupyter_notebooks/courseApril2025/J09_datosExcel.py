# -*- coding: utf-8 -*-
"""
Procesamiento de Datos usando Pandas

Autor Gabriel Ruiz Martínez
"""


# Importando paquetes
import pandas as pd
from pandas import Timestamp

"""Los valores de los parámetros que se requieren para cargar los
datos en un DataFrame se almacenarán en una variable para que 
el programa sea más genérico y pueda utilizarse, no solo en caso, sino en varios.
"""

# Guardando en variable el nombre de archivo a abrir
namefile = 'BASES_FORMULACION.xlsx'

# Guardando en variable el numero de la linea donde se encuentran los encabezados de los datos
row_encab = 4

"""
Cuando usamos un archivo que contiene un libro electrónico con hojas de cálculo es posible que se presenten casos donde solo es necesario cargar una sola hoja o todo el libro. En Pandas, cuando cargamos solamente una página electrónica, los datos se almacenarán en un DataFrame. Por otra parte, si se cargan todas las hojas del libro o un conjunto de ellas, los datos se guardarán en un diccionario de DataFrames; las etiquetas serán los números enteros que corresponden a las hojas electrónicas y los valores serán los DataFrames.

Para específicar las hojas de cálculo que se exportarán a un DataFrame, se puede indicar el nombre de la hoja electrónica o usar el número entero que corresponde a la página del libro, recordando que el número de la primera página será cero. En Pandas, mediante una lista se puede indicar un conjunto de páginas a exportar, ya sea con los nombres o el número de página del libro.  Por ejemplo para seleccionar la primera página, con el nombre de 'CLIENTE 1', tenemos las siguientes opciones:
sheet_data = 'CLIENTE 1'
sheet_data = 0

Imaginemos que se tiene un libro de 5 hojas, con etiquetas H1, H2, ... H5 y 
deseamos trabajar solo con un conjunto de ellas:
sheet_data = ['H1', 'H2', 'H3']
sheet_data = [0, 2, 'H5']
sheet_data = [0, 2, 4]

Si deseamos cargar todo el libro electrónico:
sheet_data = [0, 1, 2, 3, 4]
sheet_data = ['H1', 'H2', 'H3', 'H4', 'H5']
sheet_data = ['H1', 'H2', 2, 3, 4]
sheet_data = None

Observa que si usas en el método `read_excel` y en el parámetro `sheet_name`
específicas una lista, obtendrás un diccionario de DataFrames.
"""
# Proporcionando solamente una hoja con los datos de interes,
sheet_data = 'CLIENTE 1'
#sheet_data = 0

#  Por medio del parámetro `usecols`, se puede indicar a Pandas las columnas que deseamos exportar de la base de datos. La manera de específicar las columnas es similar a lo mencionado en la importación de las hojas electrónicas, es decir se puede utilizar los nombres de los encabezados o el número entero que corresponde al orden de las columnas. Si deseamos importar todas las columnas, especificar `None`.
# Especificando que deseamos exportar todas las columnas
columnsWork = None

# En algunas ocasiones, nuestra base de datos contiene celdas vacías, cuando se presente este caso, debemos indicar como se tratarán e identificarán estos datos pérdidos. A continuación, en una variable almacenamos el string que indicará como deben reconocerse las celdas vacías.
# String para reconocimiento de datos perdidos
nanRecog = 'nan'

# Guardando los datos en un DataFrame de Pandas
datos = pd.read_excel(namefile,
                      sheet_name=sheet_data,
                      header=row_encab,
                      usecols=columnsWork,
                      na_values=nanRecog)

# Con el metodo head() por default puedo visualizar las primeras cinco lineas de mis datos
datos.head()

# Visualizando el número filas y datos que tiene la base de datos
print(f'La base de datos tiene {datos.shape[0]} lineas y {datos.shape[1]} columnas')

# Con el metodo tail() por default puedo visualizar las ultimas cinco lineas de mis datos
datos.tail()

# Verificando información básica del DataFrame
datos.info()

# Verificando los indices
print(datos.index)

# Asignando un nombre a la columna de los indices
datos.index.name = 'No.'
datos.head(3)

# Revisando el contenido del objeto que almacena las etiquetas de las columnas
print(datos.columns)

# Cambiando el nombre de algunas columnas
datos.rename(columns={'SUBRAMO': 'Subramo', 'TRAMITE':'tramite'})
datos.head(3)


# Eliminando columnas
datos.drop(columns=['SUBRAMO'])


# Ordenando los renglones por columna (ascendente)
sortAsc = datos.sort_values(by='PAGADO')

# Ordenando los renglones por columna (descendente)
sortDes = datos.sort_values(by='PAGADO', ascending=False)

# Almacenando en variable una columna para analisis
datos2 = datos.copy()
datosF = datos2.sort_values('FECHA DE PRIMER GASTO', inplace=True)
dateFirstpay = datos2['FECHA DE PRIMER GASTO']

# Obteniendo los índices líneas de todos aquellos registros donde la fecha del primer gasto fue diferente al year 2025
iFirstpay = datos2.index[(dateFirstpay < Timestamp('2025-1-1')) & (dateFirstpay > Timestamp('2024-1-1'))]

# Almacenando datos en Series para exportar a un DataFrame de resultado
ser1 = datos2['POLIZA'][iFirstpay]
ser2 = datos2['No DE SINIESTRO'][iFirstpay]
ser3 = dateFirstpay[iFirstpay]
ser4 = datos2['TITULAR.1'][iFirstpay]

# Creando el DataFrame con el resultado del analisis
output = pd.DataFrame({'POLIZA':ser1,
                       'No DE SINIESTRO':ser2,
                       'FECHA DE PRIMER GASTO':ser3,
                       'TITULAR.1':ser4})

# Reiniciando el contador de indice
output.reset_index(names='No.', inplace=True)

# Imprimiendo filtrado
for i in range(len(output)):
    data1 = output['POLIZA'][i]
    data2 = output['No DE SINIESTRO'][i]
    data3 = output['TITULAR.1'][i]
    data4 = output['FECHA DE PRIMER GASTO'][i].strftime('%d/%m/%Y')
    print(f'Poliza: {data1}, # de Siniestro: {data2}, Nombre del Titular: {data3}. Fecha del primer gasto: {data4}')

# Exportando hacia archivo
output.to_excel('output.xlsx',
                sheet_name='Resultados',
                columns= ['POLIZA', 'No DE SINIESTRO', 'TITULAR.1', 'FECHA DE PRIMER GASTO' ],
                index=False, 
                index_label=False)

# Generando un DataFrame Nuevo
result2 = pd.DataFrame({'No DE SINIESTRO':datos2['No DE SINIESTRO'][iFirstpay],
                       'PAGADO':datos2['PAGADO'][iFirstpay],
                       'COASEGURO':datos2['COASEGURO'][iFirstpay],
                       'IVA':datos2['IVA'][iFirstpay]})

# Exportando hacia archivo
file_resul = 'resultados2.xlsx'

with pd.ExcelWriter('output1.xlsx', datetime_format='YYYY-MM-DD') as writer:
    output.style\
        .background_gradient(cmap='YlGn')\
        .to_excel(writer, index=False, sheet_name='Resultados')
        
# Generando un DataFrame Nuevo
result2 = pd.DataFrame({'No DE SINIESTRO':datos2['No DE SINIESTRO'][iFirstpay],
                       'PAGADO':datos2['PAGADO'][iFirstpay],
                       'COASEGURO':datos2['COASEGURO'][iFirstpay],
                       'IVA':datos2['IVA'][iFirstpay]})

# Exportando hacia archivo
file_resul = 'resultados2.xlsx'

# Exportando los DataFrames a una hoja de excel.
with pd.ExcelWriter(file_resul, datetime_format='YYYY-MM-DD') as writer:
    output.to_excel(writer, index=False, sheet_name='Analisis1')
    result2.to_excel(writer, index=False, sheet_name='Analisis2')

print('Se han exportado los resultados a un archivo de Excel!')
