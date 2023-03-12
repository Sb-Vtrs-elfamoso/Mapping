"""
#########################################################
            Code Lidar Hokuyo URG-04LX-UG01
#########################################################

Code Effectuant la reconnaissance d'obstacles proches et l'affichage des points en temps réel

En output on obtient l'image de ce que "voit" le lidar en temps réel (180° le coté "aveugle" du lidar (avec la languette))
Avec la detection des balises en temps réel

Sébastien Vouters, may 2022

"""
import serial # lib serial classique
import hokuyo # lib constructeur instructions lidar
import serial_port # lib constructeur communication serial lidar
import matplotlib.pyplot as plt
import math

# Variables à modifier suivant les paramètres du Robot
SEUIL_MINIMUM_DETECTION=10

# Detection du centre de la balise
#def detect_balise (map_lidar) :
 #   for (angle, distance) in map_lidar:
        

# Affichage de la detection de la balise


# Detection de 3 balises


# Affichage des 3 balises


# Verification distances des balises


# Detection du rectangle


# Affichage du rectangle



# Initialisation communication avec le protocole SCIP2.0
uart_port = '/dev/ttyACM0' #linux
#uart_port = 'COM8' # Windows : à modifier à chaque rebranchement
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


# Détection continue jusqu'a interruption Ctrl-c (SIGINT)
try:
    while (True):
        gen = laser.get_single_scan() #Lecture du Lidar (renvoie dict{angle:distance})

        x = []
        y = []
            
        # Calcul des points
        for angle, distance in gen.items():
            #angle=-i[0] # en degrés ; le moins "retourne" l'image pour l'obtenir dans le bon sens
            #distance=i[1] # en mm
            if (distance>=SEUIL_MINIMUM_DETECTION): # Ne prend pas en compte les valeurs trop proches
                x.append(distance * math.cos(math.radians(angle)))
                y.append(distance * math.sin(math.radians(angle)))
        
        # Affichage toujours bien cadre
        plt.clf()
        plt.ylim(0,3500)
        plt.xlim(-1000,1000)
        plt.scatter(y,x,s=0.5)
        
        # Attente + lecture touche appuyee
        plt.pause(0.2)
except KeyboardInterrupt:
    pass

# Affichage temps réel
plt.show()

# Arrêt Lidar
print(laser.reset())
print('---')
print(laser.laser_off())
