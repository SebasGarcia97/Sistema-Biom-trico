from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User


# Create your views here.
def registro(request):	
	if request.method == 'POST':
		username=request.POST['username']
		password=request.POST['password']
		firstname=request.POST['first_name']
		lastname=request.POST['last_name']
		email=request.POST['email']
		x=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email)
		x.save()
		print("USUARIO CREADO")
		return redirect('usuarios:Inicio')     
	else:
		print("hola")
		return render(request,'Usuario/reg_usuario.html')


	
	
def inicio(request):
	if request.method == 'POST':
		username1=request.POST['username']
		password1=request.POST['password']
		from django.contrib import auth
		x=auth.authenticate(username=username1,password=password1)
		if x is None:
			return redirect('usuarios:Inicio')   
		else:
			return redirect('usuarios:Sistema')   
	else:
		return render(request,'inicio.html')

def salir(request):
	return render(request,'inicio.html')

def info_admin(request):
	users = User.objects.all()
	return render(request,'Usuario/info_admin.html',{'users':users})

def elim_admin(request,id):
    users = User.objects.get(id = id)
    users.delete()
    return redirect('usuarios:info_admin')
	
#BASE DE DATOS



def sistema(request):
	return render(request,'sistema.html')
