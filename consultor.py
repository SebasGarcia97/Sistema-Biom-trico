import time
from datetime import date, datetime
from AppEmpleados.models import *
from django.db import close_old_connections


class BaseDatos:
    # Constructor
    def __init__(self):
        # Variables globales
        self.empleados = None
        self.registro = None
        self.connection = None

    # Funcion para marcar entrada
    def marcarEntrada(self, id_in):
        comp = list(Controlpersonal.objects.filter(emp_id = id_in, mar_estado = 0))
        print(len(comp))

        print(id_in)
        print(date.today())
        print(time.strftime("%H:%M:%S"))
        
        if len(comp)==0:
            Controlpersonal.objects.create(emp_id = id_in, mar_fecha = date.today(), mar_hora_entrada = time.strftime("%H:%M:%S"), mar_estado = 0)
            return True
        else:
            return False
   
    # Funcion para marcar salida
    def marcarSalida(self, id_in):
        comp = Controlpersonal.objects.filter(emp_id = id_in, mar_estado = 0)
        l_comp = list(comp)
        
        if len(l_comp)!=1:
            return False
        else:
            comp.update(mar_hora_salida = time.strftime("%H:%M:%S"), mar_estado = 1)
            return True

    def horario(self):
        marcaciones = Marcar.objects.all()
        return marcaciones

    def estado_sistema(self):
        close_old_connections()
        hora_actual = datetime.now().time()
        reglas=Reglas_Marcacion.objects.first()

        hi1 = reglas.hi1
        hi2 = reglas.hi2
        hi3 = reglas.hi3
        hi4 = reglas.hi4
        ho1 = reglas.ho1
        ho2 = reglas.ho2
        ho3 = reglas.ho3
        ho4 = reglas.ho4

        if (hi1 < hora_actual and hi2 > hora_actual) or (hi3 < hora_actual and hi4 > hora_actual):
            return "Entrada"
        elif (ho1 < hora_actual and ho2 > hora_actual) or (ho3 < hora_actual and ho4 > hora_actual):
            return "Salida"
        else:
            return "Cerrado"