# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Controlpersonal(models.Model):
    mar_fecha = models.DateField()
    mar_hora_entrada = models.TimeField()
    mar_hora_salida = models.TimeField()
    mar_estado = models.IntegerField(null=True)
    emp_id = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'Controlpersonal'


class Empleado(models.Model):
    primer_nombre = models.CharField(max_length=20)
    segundo_nombre = models.CharField(max_length=20)
    primer_apellido = models.CharField(max_length=20)
    segundo_apellido = models.CharField(max_length=20)
    cargo = models.CharField(max_length=20)
    cedula = models.CharField(unique=True, max_length=10)
    celular = models.CharField(unique=True, max_length=10)
    email = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = 'Empleado'


class Administradores(models.Model):
    adm_id = models.BigAutoField(primary_key=True)
    adm_username = models.CharField(unique=True, max_length=50)
    adm_password = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'administradores'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Emp(models.Model):
    emp_id = models.BigAutoField(primary_key=True)
    emp_cedula = models.CharField(unique=True, max_length=10)
    emp_nombre = models.CharField(max_length=50)
    emp_apellido = models.CharField(max_length=50)
    emp_celular = models.CharField(max_length=10)
    emp_correo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'emp'

class Registro(models.Model):
    reg_id = models.BigAutoField(primary_key=True)
    emp = models.ForeignKey(Emp, models.DO_NOTHING)
    reg_fecha_entrada = models.DateField()
    reg_hora_entrada = models.TimeField()
    reg_fecha_salida = models.DateField()
    reg_hora_salida = models.TimeField()
    reg_estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registro'

class Marcar(models.Model):
    emp_id = models.IntegerField(max_length=11)
    primer_nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    mar_fecha = models.DateField()
    mar_hora_entrada = models.TimeField()
    mar_hora_salida = models.TimeField()
    mar_estado = models.IntegerField(max_length=1)

    class Meta:
        managed = False
        db_table = 'Marcar'
