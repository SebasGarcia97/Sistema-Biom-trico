from django.shortcuts import render,HttpResponse,redirect
<<<<<<< HEAD
from AppEmpleados.forms import EmpleadoForm
from AppEmpleados.models import Empleado, Marcar
=======
from AppEmpleados.forms import EmpleadoForm, ControlPersonalForm
from AppEmpleados.models import Empleado, Controlpersonal
>>>>>>> 46e95be9ff9ed5cd99dc6515f74d78569976bd62
from AppEmpleados.camera import VideoCamera
from django.http.response import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import time, datetime

from consultor import BaseDatos

consultor = BaseDatos()

global idv
idv=1
global cont
cont=0
# Create your views here.
def sistema(request):
	global idv
<<<<<<< HEAD
	ultimaMarcacion = Marcar.objects.filter(emp_id=idv).last()
	hora = ultimaMarcacion.mar_hora_entrada
	hora1 = ultimaMarcacion.mar_hora_salida
	if not hora1:
		hora1 = "No registrado"
=======
	hora= datetime.now()
>>>>>>> 46e95be9ff9ed5cd99dc6515f74d78569976bd62
	empleados = Empleado.objects.filter(id=idv)
	if idv==0:
		hora=""
		hora1=""
	return render(request,'sistema.html',{'hora':hora,'hora1':hora1,'empleados':empleados})

def informacion(request):
	empleados = Empleado.objects.all()
	return render(request,'Empleados/informacion.html',{'empleados':empleados})
  
def reg_empleados(request):	
	if request.method == "POST":
		empleado_form = EmpleadoForm(request.POST)
		if empleado_form.is_valid():
			empleado_form.save()
			return redirect('empleados:Video')             
	else:
		empleado_form = EmpleadoForm()
	return render(request,'Empleados/reg_empleados.html',{'empleado_form':empleado_form})

def modificarEmpleado(request,id):
	editar = Empleado.objects.get(id = id)	  
	empleado_form = EmpleadoForm(instance=editar)	
	return render(request,'Empleados/modificar_empleados.html',{'empleado_form':empleado_form,'editar':editar})

def editarEmpleado(request,id):
	editar = Empleado.objects.get(id = id)	  
	empleado_form = EmpleadoForm(request.POST,instance=editar)	
	if empleado_form.is_valid():
		empleado_form.save()
	empleados = Empleado.objects.all()
	return render(request,'Empleados/informacion.html',{'empleado_form':empleado_form,'empleados':empleados})

def elim_empleados(request,id):
	empleado = Empleado.objects.get(id = id)
	empleado.delete()
	return redirect('empleados:Informacion')


#CAMARA
def Video(request):
	return render(request,'Empleados/video.html')

def gen(camera):
	while True:
		frame = camera.CapturarRostros()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

#RECONOCIMIENTO
def gen_rec(camera):
	global idv
	global hora
	idv = 0
	cont = 0
	id_aux = 0
	ban = True
	ban2 = True
	while ban == True:
		frame,idv = camera.ReconocimientoFacial()
		if str(idv)=="":
			idv=0
		else:
			idv = idv+1
		if ban2:
			id_aux = idv
			ban2 = False 
		
		if idv == id_aux:
			cont = cont + 1
			yield(b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		else:
			cont = 0
			ban2 = True

		if cont == 20:			
			marcarEntrada()
			print("SU ID es :",id_aux)
			print("LISTO")
			cont = 0
			if id_aux != 0:
				ret = consultor.marcarSalida(id_aux)


		
def reconocer(request):
	return StreamingHttpResponse(gen_rec(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')

def horario(request):
	marcacion = consultor.horario()
	return render(request,'Empleados/horario.html',{'marcacion':marcacion})

def marcarEntrada ():
	hora_entrada_inicial = time(7,0,0,0)
	hora_entrada_final = time(10,0,0,0)
	hora_marcacion = time(7,15,0,0) 
	id_persona = 5
	#mar_estado = Controlpersonal.objects.get(id = id_persona)
	#marcacion_entrada = .mar_estado
	#Controlpersonal.objects.get(id=1).mar_estado
	if hora_entrada_inicial <= hora_marcacion and hora_entrada_final >= hora_marcacion:
		Controlpersonal.objects.filter(id=id_persona).update(mar_estado = 1)
		print("MARCACION ACEPTADA")
	elif hora_entrada_inicial >= hora_marcacion:
		print("ESPERE SE HABILITA EL SISTEMA")
	elif hora_entrada_final < hora_marcacion:
		print("LLEGA TARDE")