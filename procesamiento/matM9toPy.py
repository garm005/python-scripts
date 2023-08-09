# -*- coding: utf-8 -*-
"""
Script que importa los datos de un archivo mat (Sontek Surveyor M9) a
Python. El script como salida proporcionar archivos CSV con los datos
batimetricos, asi como un archivo shapefile con la ubicacion espacial
de los puntos de muestreo.

Como inputs se deben proporcionar:
1. El nombre del archivo mat.
2. Valores delta x y y. 

Created on Mon Jul 31 13:35:43 2023
@author: Gabriel Ruiz Martinez
"""

from collections import OrderedDict
import fiona
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io as sio
import simplekml

def obj_array_to_type(arr, typ):
    """
    Convert an object array of same-sized arrays to a normal 3D array
    with dtype=typ. This is a workaround as numpy doesn't realize that
    the object arrays are numpy arrays of the same legth, so just using
    array.astype(typ) fails. Technically works if the items are numbers
    and not arrays, but then `arr.astype(typ)` should be used.
    """
    full_shape = (*arr.shape, *np.shape(arr.flat[0]))
    return np.vstack(arr.flatten()).astype(typ).reshape(full_shape)

def points2layer(inputfile, shpfile, cs):
    '''
    Script que exporta PUNTOS de un archivo csv a un archivo shapefile,
    creandose los archivos .dbf, .prj, .shp y .shx.
    Se requieren los modulos fiona y pandas. El archivo csv que se usara para         
    generar la tabla de atributos debera tener 1 linea de encabezados y 3 
    columnas, en el siguiente orden y nombre del encabezado:
    1. coordenadas de longitud (Lon), 
    2. coordenadas de latitud (Lat), 
    3. etiqueta del punto (Etiqueta).
    
    Argumentos de la funcion:
    inputfile: nombre del archivo csv con los puntos,
               incluir la extension del archivo.
    shpfile: nombre del shapefile (este nombre se 
             exportara como el nombre de la capa)
             no incluir la extension de archivo.
    cs = Sistema de referencia geografico de los puntos.
             
    Ejemplo:
        inputfile = 'PtosPista.csv'
        shpfile = 'PuntosPista'
        cs = 'WGS84'

        points2layer(inputfile,shpfile,cs)
    Gabriel Ruiz, 2022. IMTA.
    '''
    
    try:
        # Abriendo el archivo de datos y guardando en un dataframe de Pandas
        if inputfile[-1] == 'z':   # xyz
            datos = pd.read_csv(inputfile, header = 0, sep = ' ')
            datacsv = 0;
            schema = {
                'geometry': 'Point',
                'properties': OrderedDict([
                    ('ID', 'int'),
                    ('Nombre', 'str'),
                    ('X/Lon', 'float'),
                    ('Y/Lat', 'float'),
                    ('Z', 'float'),
                    ('Cuerpo', 'str')
                    ])
                }            
        else:                      # cvs
            datos = pd.read_csv(inputfile, header = 0, sep = ',')
            datacsv = 1;
            
            # Definiendo el esquema que requiere fiona para la 
            #exportación de la tabla de atributos
            schema = {
                'geometry': 'Point',
                'properties': OrderedDict([
                    ('ID', 'int'),
                    ('Nombre', 'str'),
                    ('X/Lon', 'float'),
                    ('Y/Lat', 'float')
                    ])
                }

        # Estableciendo el sistema de referencia
        if cs == 'WGS84':
                sc = 'EPSG:4326'
        elif cs == 'UTM_13N':
                sc = 'EPSG:32613'
        elif cs == 'UTM_14N':
                sc = 'EPSG:32614'
        elif cs == 'UTM_15N':
                sc = 'EPSG:32615'
        elif cs == 'UTM_16N':
                sc = 'EPSG:32616'
              
        # Almacenando en tupla el no. de filas y columnas del dataframe
        nf = datos.shape

        # Creando la colleccion que se usara para exportar los datos
        pto2shp = fiona.open(shpfile+'.shp', 
                             mode = 'w', 
                             driver = 'ESRI Shapefile', 
                             schema = schema, 
                             crs = sc)
        
        # Exportando los datos, via diccionario, a la coleccion de fiona
        if datacsv == 1:
            for i in range(nf[0]):
                dicdatos = {
                    'geometry': {'type': 'Point', 
                                 'coordinates': (datos.Lon[i],
                                                 datos.Lat[i])},
                    'properties':{'ID': i, 
                                  'Nombre': datos.Etiqueta[i],
                                  'X/Lon': datos.Lon[i],
                                  'Y/Lat': datos.Lat[i]} }
                pto2shp.write(dicdatos)
        else:
            for i in range(nf[0]):
                
                if datos.iloc[i,2] < 0:
                    cuerpo = 'Tierra'
                else:
                    cuerpo = 'Agua'
                    
                dicdatos = {
                    'geometry': {'type': 'Point', 
                                 'coordinates': (datos.iloc[i,0],
                                                 datos.iloc[i,1])},
                    'properties':{'ID': i, 
                                  'Nombre': 'Punto' + str(i),
                                  'X/Lon': datos.iloc[i,0],
                                  'Y/Lat': datos.iloc[i,1],
                                  'Z': datos.iloc[i,2],
                                  'Cuerpo': cuerpo
                                  } }
                pto2shp.write(dicdatos)

        # Cerrando la coleccion fiona (cerrando archivos creados)
        pto2shp.close()
        print('Los puntos se han enviado a un archivo SHP.')
    except:
        print('Error en la funcion')  
    return


# Inputs
nfile = '20230719091839'
dx = 100 

datos = sio.loadmat(nfile, appendmat=True, struct_as_record=True,
                    squeeze_me=True)

dBT = datos["BottomTrack"]["BT_Depth"]
dBT1d = dBT.flatten()
dBT1d = np.vstack(dBT1d)
dBT = dBT1d.reshape(dBT1d.size)
del dBT1d

dvb = datos["BottomTrack"]["VB_Depth"]
dVb = np.vstack(dvb.flatten())
dVB = dVb.reshape(dVb.size)
del dvb, dVb

longi = datos["GPS"]["Longitude"]
longit = np.vstack(longi.flatten())
lon = longit.reshape(longit.size)
del longi, longit

latid = datos["GPS"]["Latitude"]
lati = np.vstack(latid.flatten())
lat = lati.reshape(lati.size)
del latid, lati

utmd = datos["GPS"]["UTM"]
utm1 = np.stack(utmd.flatten())
utm = utm1.reshape(utm1.size)
del utmd, utm1

yind = np.where(utm > 1000000)
y = utm[yind]
xind = np.where(utm < 600000)
x = utm[xind]
del yind, xind

num_datos = lon.size

dat_zero = np.where(dBT <= 0)

print('El archivo {}.mat contiene {} registros.'.format(nfile, num_datos))
if dat_zero[0].size > 0:
    print('Sin embargo:')
    print('El archivo contiene {} registros con ceros en la profundidad,'.format(
        dat_zero[0].size))
    print('estos registros no serán exportados!')
    element = np.arange(num_datos)
    lon = lon[~np.isin(element, dat_zero)]
    lat = lat[~np.isin(element, dat_zero)]
    x = x[~np.isin(element, dat_zero)]
    y = y[~np.isin(element, dat_zero)]
    dBT = dBT[~np.isin(element, dat_zero)]
    dVB = dVB[~np.isin(element, dat_zero)]
    print('Despues del filtrado se tienen {} registros.\n'.format(dBT.size))

print('Información:')
print('Profundidad min: {0:8.3f} m'.format(np.min(dBT)))
print('Profundidad max: {0:8.3f} m'.format(np.max(dBT)))
z_range = np.arange(0, np.ceil(np.max(dBT)), 1, dtype=int)
n_depths = np.zeros(z_range.size)
etiq = []

for i in range(z_range.size):
    if i < z_range.size-1:
        temp = np.logical_and((dBT >= z_range[i]), (dBT < z_range[i+1]))
        n_depths[i] = np.extract(temp, dBT).size
        print('Registros con profundidad de {} m a {} m: {}'.format(z_range[i],
            z_range[i+1], int(n_depths[i])))
        etiq.append(str(z_range[i])+' a '+ str(z_range[i+1]))
    else:
        temp = np.where(dBT > z_range[i])
        n_depths[i] = temp[0].size
        print('Registros con profundidad de {} m a {} m: {}\n'.format(z_range[i],
            z_range[i]+1, int(n_depths[i])))
        etiq.append(str(z_range[i])+' a '+ str(z_range[i]+1))

plt.style.use('seaborn')
plt.figure()
plt.plot(-dBT, color='r')
plt.xlabel('No. de registro')
plt.ylabel('Profundidad (m)')
plt.xlim([0, dBT.size])
plt.savefig(fname=nfile+'_Rec.png', dpi='figure', format='png')

plt.figure()
plt.bar(etiq, n_depths)
plt.xlabel('Profundidades (m)')
plt.ylabel('Datos')
plt.savefig(fname=nfile+'_Bar.png', dpi='figure', format='png')

# Zona de procesamiento de los valores de z





#----------------------------------------

dataGEO = pd.DataFrame({'lon(°)':lon, 'lat(°)':lat, 'BT(m)':dBT, 'VB(m)':dVB})
dataUTM = pd.DataFrame({'x(m)':x, 'y(m)':y, 'BT(m)':dBT, 'VB(m)':dVB})
                  
print('Revisando el orden de los datos que seran exportados:')   
print(dataGEO.head())
print('.\n.\n.\n')
print(dataGEO.tail())
print('')
print(dataUTM.head())
print('.\n.\n.\n')
print(dataUTM.tail())
print('')

dataGEO.to_csv(nfile+'_GEO.csv', header=True, index=False)
dataUTM.to_csv(nfile+'_UTM.csv', header=True, index=False)

del datos
eti = []
for i in range(lon.size):
    eti.append('P'+str(i+1))
    
dataGEO2 = pd.DataFrame({'Lon':lon, 'Lat':lat, 'Etiqueta':eti})
print(dataGEO2.head())
print('.\n.\n.\n')
print(dataGEO2.tail())
print('')
dataGEO2.to_csv(nfile+'_GEO2.csv', header=True, index=False)
points2layer(nfile+'_GEO2.csv', nfile+'_GEOPoints', 'WGS84')

kml = simplekml.Kml()
for i in range(dataGEO2.shape[0]):
    pto = kml.newpoint()
    pto.name = dataGEO2['Etiqueta'][i]
    pto.coords =[(dataGEO2['Lon'][i], dataGEO2['Lat'][i])]
kml.save(nfile+'.kml')
print('Los puntos se han enviado a un archivo kml')

lomin = dataGEO["lon(°)"].min()
lomax = dataGEO["lon(°)"].max()
lamin = dataGEO["lat(°)"].min()
lamax = dataGEO["lat(°)"].max()

print('\nBordes del area de interes, en coordenadas geograficas:')
print('Esquina Inferior Izquierda: {}, {}'.format(lomax, lamin))
print('Esquina Inferior Derecha: {}, {}'.format(lomin, lamin))
print('Esquina Superior Izquierda: {}, {}'.format(lomax, lamax))
print('Esquina Superior Derecha: {}, {}'.format(lomin, lamax))

xmin = dataUTM["x(m)"].min()
xmax = dataUTM["x(m)"].max()
ymin = dataUTM["y(m)"].min()
ymax = dataUTM["y(m)"].max()

llon = lomax - lomin
llat = lamax - lamin

lx = xmax - xmin
ly = ymax - ymin

print('\nDimensiones del area muestreada:')
print('Distancia horizontal: {}° ó {:8.3f} m'.format(llon, lx))
print('Distancia vertical: {}° ó {:8.3f} m'.format(llat, ly))
