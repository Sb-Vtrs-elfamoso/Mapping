"""
#########################################################
            Code Lidar Hokuyo URG-04LX-UG01
#########################################################

Code Effectuant la reconnaissance d'obstacles proches et l'affichage des points en temps réel

En output on obtient l'image de ce que "voit" le lidar en temps réel (180° le coté "aveugle" du lidar (avec la languette))

Sébastien Vouters, may 2022

"""
import serial # lib serial classique
import hokuyo # lib constructeur instructions lidar
import serial_port # lib constructeur communication serial lidar
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from scipy.signal import convolve2d

# Variables à modifier suivant les paramètres du Robot
LARGEUR_ROBOT=400 # en mm pour notre robot
LONGUEUR_ROBOT=400 # en mm pour notre robot
#SEUIL_MINIMUM_DETECTION=(min(LARGEUR_ROBOT,LONGUEUR_ROBOT)-10)/2 # valeurs en dessous de ce seuil non comptabilisées (-10 pour marge d'erreur)
SEUIL_MINIMUM_DETECTION=5
LARGEUR_ROBOT_NORME=400 # en mm pour la réglementation de la compétition
LONGUEUR_ROBOT_NORME=400 # en mm pour la réglementation de la compétition
ALERTE_DETECTION=SEUIL_MINIMUM_DETECTION+(min(LARGEUR_ROBOT_NORME,LONGUEUR_ROBOT_NORME)+10)/2

# Initialisation communication avec le protocole SCIP2.0
#uart_port = '/dev/ttyACM0' linux
uart_port = 'COM8' # Windows : à modifier à chaque rebranchement
uart_speed = 19200
laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed, timeout=0.2)
port = serial_port.SerialPort(laser_serial)

# Initialisation Lidar
laser = hokuyo.Hokuyo(port)
print(laser.laser_on())
print('---')
print(laser.set_high_sensitive(False))
print('---')
print(laser.set_motor_speed(200))
print('---')

# Initialisation graphique
figure = plt.figure()
plt.clf()
plt.ylim(-2000,2000)
plt.xlim(-2000,2000)

x_m = []
theta_m = []
y_m = []
rho_m = []
compter_m = []

# Détection continue jusqu'a interruption Ctrl-c (SIGINT)
try:
    f = open("data.txt", "a")
    count = 0
    while (count<10):
        gen = laser.get_single_scan() #Lecture du Lidar (renvoie dict{angle:distance})
        
        x = []
        y = []
        theta = []
        rho = []
        compter = []

        donnees = []
        # Calcul des points
        for i in gen.items():
            angle=-i[0] # en degrés ; le moins "retourne" l'image pour l'obtenir dans le bon sens
            distance=i[1] # en mm
            if (distance>=SEUIL_MINIMUM_DETECTION): # Ne prend pas en compte les valeurs trop proches
                x.append(distance * math.cos(math.radians(angle)))
                y.append(distance * math.sin(math.radians(angle)))
                theta.append(angle)
                rho.append(distance)
                compter.append(count)
        
        # Affichage toujours bien cadre
        #plt.clf()
        plt.ylim(-500,500)
        plt.xlim(-500,500)
        plt.plot(x,y,'bo', markersize=1)

        x_m.append(x)
        theta_m.append(theta)
        y_m.append(y)
        rho_m.append(rho)
        compter_m.append(compter)

        for i in zip(theta_m, rho_m,x_m, y_m,compter_m):
            for indiv in zip(i[0], i[1], i[2], i[3], i[4]):
                donnees.append(indiv)
            
        
        #df_measure = pd.DataFrame(data=donnees, columns=['dist', 'angle', 'x', 'y'])
        
        if count == 20:
            count=0
            plt.clf()
        # Attente + lecture touche appuyee
        plt.pause(0.001)
        count += 1

        combined_list = list(zip(x, y))
        # apply the Wiener filter
        """kernel = [[0.25, 0, 0.25],
                  [0, 0.5, 0],
                  [0.25, 0, 0.25]]
        filtered_image = convolve2d(combined_list, kernel)
        
        # display the filtered image
        plt.clf()
        plt.imshow(filtered_image)
        plt.ylim(-3000,3000)
        plt.xlim(-3000,3000)
        plt.plot(x,y)
        """
except KeyboardInterrupt:
    pass

# Affichage temps réel
plt.show()
f.close()

# Arrêt Lidar
print(laser.reset())
print('---')
print(laser.laser_off())

df_measure = pd.DataFrame(data=donnees, columns=['dist', 'angle', 'x', 'y', 'sample'])
df_measure.to_csv(r"C:\Users\sBTvR\Documents\INSA\Club Robot\Lidar_Test\data.csv", index=False)
