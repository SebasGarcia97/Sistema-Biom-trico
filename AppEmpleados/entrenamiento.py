import cv2,os,urllib.request
import numpy as np
from django.conf import settings
#from AppEmpleados.models import Empleado
import imutils
import threading

dataPath = './Data' #Cambia a la ruta donde hayas almacenado Data
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)
labels = []
facesData = []
label = 0
for nameDir in peopleList:
    personPath = dataPath + '/' + nameDir
    print('Leyendo las imágenes')

    for fileName in os.listdir(personPath):
        print('Rostros: ', nameDir + '/' + fileName)
        labels.append(label)
        facesData.append(cv2.imread(personPath+'/'+fileName,0))
    label = label + 1

# Métodos para entrenar el reconocedor
face_recognizer = cv2.face.FisherFaceRecognizer_create()

# Entrenando el reconocedor de rostros
print("Entrenando...")
face_recognizer.train(facesData, np.array(labels))
# Almacenando el modelo obtenido
face_recognizer.write('modeloFisherFace.xml')
print("Modelo almacenado...")
