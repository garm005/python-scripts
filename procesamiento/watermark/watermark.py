# -*- coding: utf-8 -*-
"""
Script that 1) inserts a watermark in a jpg image. The 
watermark has data imported from a Excel file.
2) The original image is resized to 8 and 6 cm.
3) The image resized and with the watermark is saved in 
png file.

The PILLOW module must be installed in the computer.


Created on Sat Oct 7 11:18:49 2023

@author: Gabriel Ruiz
"""

# Importing the modules
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# ************* Inputs ****************
# Excel filename
fileExcel = 'Puntos_utm.xlsx'

# Dimensions to the resize the image (in cms)
largo = 8
ancho = 6

# Watermark coordinates (in pixels) (Left Top Corner)
x = 260
y = 155
#x = 800
#y = 570

# Font path to water mark
pathFont = 'C:\Windows\Fonts\Montserrat\Montserrat-Bold.ttf'
# *************************************

# Creating the tuple with the watermark coordinates
wpos = tuple([x, y])

# Getting the pixels value from the resize dimensions
tam = [int(np.floor(largo*(96/2.54))), 
       int(np.floor(ancho*(96/2.54)))]

# Importing the data from Excel file
try:
    datos = pd.read_excel(fileExcel,
                      header=0,
                      usecols=[1, 2, 3, 4, 5, 6],
                      parse_dates=True,            
                      engine='openpyxl')
except OSError:
    print('Hay un problema con el archivo de Excel, no se pudo cargar')

for f in os.listdir(os.getcwd()):
    if f.endswith('.jpg') and f[0] == 'p':
        
        print('Procesando archivo: {:s}'.format(f))
        
        # Knowing the point and number of the picture
        noPoint = f[2:5]
        noFoto = f[6:8]
        
        # Finding the index in the Dataframe that corresponds to the point
        try:
            ptoIndex = datos.index[datos['No'] == int(noPoint)][0]
            
            # Importing the image to Python and reducing the dimensions
            try:
                # Opening the image
                with Image.open(f) as im:
                    #im.show()
                    im.thumbnail(tam, Image.Resampling.LANCZOS)
                    #im.save('a.jpg','JPEG')
                    plt.imshow(im)
                # Creating a copy of the image. This copy will be used to 
                # to insert the watermark
                imaEdit = im.copy()
            
                # Creating the object that will be used to "draw" the  watermark
                imagen = ImageDraw.Draw(imaEdit)

                # Setting the watermark font
                tipo = ImageFont.truetype(font=pathFont, 
                                          size=8, 
                                          encoding='unic')
            
                # Info of the watermark
                xutm = str(np.floor(datos.iloc[ptoIndex][0]*100)/100)
                yutm = str(np.floor(datos.iloc[ptoIndex][1]*100)/100)
                pto = str(int(datos.iloc[ptoIndex][2]))
                dia = str(datos.iloc[ptoIndex][3].day)
                mes = str(datos.iloc[ptoIndex][3].month)
                year = str(datos.iloc[ptoIndex][3].year)
            
                if datos.iloc[ptoIndex][4].hour <= 9:
                    hora = '0' + str(datos.iloc[ptoIndex][4].hour)
                else:
                    hora = str(datos.iloc[ptoIndex][4].hour)
                if datos.iloc[ptoIndex][4].minute <= 9:
                    minuto = '0' + str(datos.iloc[ptoIndex][4].minute)
                else:
                    minuto = str(datos.iloc[ptoIndex][4].minute)
                
                frente = datos.iloc[ptoIndex][5]
            
                # Watermark text
                marca_agua = 'Tramo 7\n'+'X = ' + xutm + '\n' + 'Y = ' + yutm+\
                         '\n' + 'Observacion P:' + pto + '\n' + dia + '/' + \
                          mes + '/' + year + ' ' + hora + ":" + minuto + '\n'+\
                          frente
                          
                # Adding the watermark in the image
                imagen.multiline_text(wpos, 
                                  marca_agua,
                                  fill=None,
                                  font=tipo,
                                  anchor='ms',
                                  spacing=0,
                                  align='left',
                                  stroke_fill='black',
                                  stroke_width=1)
                
                # Exporting the image to png image
                imaEdit.save('p_' + noPoint + '_' + noFoto + '.png', 'PNG')
                #imaEdit.show()        
                
            except OSError:
                print('Hay un problema al abrir la imagen')
            
        except:
            print('El archivo {:s} es un punto que'.format(f))
            print('no se encuentra en la base de datos!')
            