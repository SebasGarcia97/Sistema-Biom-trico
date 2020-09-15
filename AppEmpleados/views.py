from django.shortcuts import render,HttpResponse,redirect
from AppEmpleados.forms import EmpleadoForm
from AppEmpleados.models import Empleado
from AppEmpleados.camera import VideoCamera
from django.http.response import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
global idv
idv=1
global cont
cont=0
# Create your views here.
def sistema(request):
	global idv
	empleados = Empleado.objects.filter(id=idv)
	return render(request,'sistema.html',{'empleados':empleados})

def informacion(request):
	empleados = Empleado.objects.all()
	return render(request,'Empleados/informacion.html',{'empleados':empleados})
  
#BASE DE DATOS
def reg_empleados(request):
	if request.method == "POST":
		empleado_form = EmpleadoForm(request.POST)
		if empleado_form.is_valid():
			empleado_form.save()
			return redirect('empleados:Video')             
	else:
		empleado_form = EmpleadoForm()
	return render(request,'Empleados/reg_empleados.html',{'empleado_form':empleado_form})

def editarEmpleado(request,id):
	empleado_form= None
	error = None
	try:
		editar = Empleado.objects.get(id = id)
		if request.method == 'GET':
			empleado_form= EmpleadoForm(instance = editar)            
		else:
			empleado_form = EmpleadoForm(request.POST, instance = editar)
			print("empleado_form",empleado_form)   
			if empleado_form.is_valid():
				empleado_form.save()
	except ObjectDoesNotExist as e:
		error = e        
	return render(request,'Empleados/reg_empleados.html',{'empleado_form':empleado_form,'error':error})

def elim_empleados(request,id):
	empleado = Empleado.objects.get(id = id)
	empleado.delete()
	#empleado.estado = False
	#empleado.save()
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
			#print(cont)
			#print(id_aux)
			yield(b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		else:
			cont = 0
			ban2 = True

		if cont == 20:
			print("SU ID es :",id_aux)
			empleados2 = Empleado.objects.filter(id=id_aux)
			print("LISTO")
			cont = 0
		
	#		ban = False
	#while True:
	#	frame,idv = camera.ReconocimientoFacial()
	#	if str(idv)=="":
	#		idv=0
	#	yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		
def reconocer(request):
	return StreamingHttpResponse(gen_rec(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')
	
