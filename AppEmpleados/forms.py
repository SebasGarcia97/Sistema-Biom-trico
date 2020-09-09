from django import forms
from AppEmpleados.models import Empleado

class EmpleadoForm (forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','cedula','celular','cargo','email']
        