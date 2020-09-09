from django.db import models
#python manage.py makemigrations
# python manage.py migrate
# Create your models here.
class Empleado(models.Model):
    primer_nombre=models.CharField('Primer Nombre',max_length=20, blank = False, null = False )
    segundo_nombre = models.CharField('Segundo Nombre',max_length = 20, blank = False, null = False)
    primer_apellido = models.CharField('Apellido Paterno',max_length = 20, blank = False, null = False)
    segundo_apellido = models.CharField('Apellido Materno',max_length = 20, blank = False, null = False)
    cargo = models.CharField('Cargo',max_length = 20, blank = False, null = False)
    cedula = models.CharField('Cedula',max_length = 10, blank = False, null = False, unique = True)
    celular = models.CharField('Celular',max_length = 10, blank = False, null = False, unique = True)
    email = models.EmailField('Correo Electrónico', max_length=254, unique = True)
    class Meta:
        verbose_name='Empleado'
        verbose_name_plural='Empleados'
        ordering = ['primer_nombre']

    def _str_(self):
        return self.primer_nombre

