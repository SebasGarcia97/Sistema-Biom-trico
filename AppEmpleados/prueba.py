import cv2,os,urllib.request
import numpy as np
from django.conf import settings
import imutils
from AppEmpleados.models import Empleado
import threading
global ban
ban=False
class VideoCamera(object):
	def _init_(self):               
		self.video = cv2.VideoCapture(0)
		self.count=0
	def _del_(self):
		self.video.release()
	def get_frame(self):                
		_,image = self.video.read()
		frame_flip = cv2.flip(image,1)
		_,jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()
		
	def Entrenar(self):
		global ban
		while ban==True:
			dataPath = 'C:/Users/Ismael/Desktop/SAPP/SAPP/Data/' #Cambia a la ruta donde hayas almacenado Data #Cambia a la ruta donde hayas almacenado Data
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
			ban=False
	def ReconocimientoFacial(self):
		dataPath = 'C:/Users/Ismael/Desktop/SAPP/SAPP/Data'  # Cambia a la ruta donde hayas almacenado Data
		imagePaths = os.listdir(dataPath)
		print('imagePaths=', imagePaths)
		face_recognizer = cv2.face.FisherFaceRecognizer_create()
		# Leyendo el modelo
		face_recognizer.read('C:/Users/Ismael/Desktop/SAPP/SAPP/AppEmpleados/modeloFisherFace.xml')
		cap = self.video
		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		auxFrame = gray.copy()
		faces = faceClassif.detectMultiScale(gray, 1.3, 5)
		#print (len(faces))
		result = ""
		if len(faces)!= 0:
			for (x, y, w, h) in faces:
				rostro = auxFrame[y:y + h, x:x + w]
				rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
				result = face_recognizer.predict(rostro)
			#cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
			# FisherFaces				
				if result[1] < 1500:	
					#cv2.putText(frame,'{}'.format(result),(x,y-50),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)				
				else:
					#cv2.putText(frame,'{}'.format(result),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.putText(frame,'DESCONOCIDO',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
		_,jpeg = cv2.imencode('.jpg', frame)
		#cv2.imshow('prueba',frame)
		if result != "":
			return jpeg.tobytes() , imagePaths[result[0]]
		else:
			return jpeg.tobytes() , result
			
	def CapturarRostros(self):
		global ban
		# Para crear una carpeta con el nombre de la persona donde se almacenara los rostros
		print("ENTRANDO EN FUNCION")
		id =str(Empleado.objects.count())
		personName = id
		dataPath = 'C:/Users/Ismael/Desktop/SAPP/SAPP/Data/' #Cambia a la ruta donde hayas almacenado Data
		personPath = dataPath + '/' + personName
		# Crea carpeta
		if not os.path.exists(personPath):
			print('Carpeta creada: ',personPath)
			os.makedirs(personPath)
		cap = self.video
		#cap = cv2.VideoCapture('Video.mp4')
		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
		ret, frame = cap.read()               
		frame =  imutils.resize(frame, width=640)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		auxFrame = frame.copy()
		faces = faceClassif.detectMultiScale(gray,1.3,5)
		if self.count <= 50:
			for (x,y,w,h) in faces:			
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
				cv2.imwrite(personPath + '/rotro_{}.jpg'.format(self.count),rostro)
				self.count = self.count + 1
				#cv2.imshow('frame',frame)
			_,jpeg = cv2.imencode('.jpg', frame)
			#cv2.imshow('prueba',frame)
			return jpeg.tobytes()
		else:
			if self.count==51:
				entrenamiento = threading.Thread(target=VideoCamera().Entrenar) # use default name
				ban=True
				entrenamiento.start()	
			self.count = self.count + 1
			if ban == True:
				cv2.putText(frame,"Entrenando....", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
			else:
				cv2.putText(frame,"Captura Completa, de click en terminar", (0,80), cv2.FONT_HERSHEY_SIMPLEX, 1 ,(0,0,255), 2, cv2.LINE_AA)
			_,jpeg = cv2.imencode('.jpg', frame)
			#cv2.imshow('prueba',frame)
			return jpeg.tobytes()