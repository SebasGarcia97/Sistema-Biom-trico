from django import forms
from AppEmpleados.models import Empleado,Controlpersonal

class EmpleadoForm (forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','cedula','celular','cargo','email']

class ControlPersonalForm (forms.ModelForm):
    class Meta:
        model = Controlpersonal
        fields = ['mar_fecha','mar_hora_entrada','mar_hora_salida','mar_estado','emp_id']