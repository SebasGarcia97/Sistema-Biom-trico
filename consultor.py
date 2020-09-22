import sqlalchemy as db
from sqlalchemy import and_
import pandas as pd
import time
from datetime import date


class Conexion:
    # Constructor
    def __init__(self):
        # Variables globales
        self.empleados = None
        self.registro = None
        self.connection = None
        self.conectar()

    # Conectar la BD
    def conectar(self):
        # Crea la cadena de conexion, para nuestro Script a MySQL
        engine = db.create_engine("mysql+mysqlconnector://admin_sapp:sappsapp@techsolutionsec.ga:3306/admin_sapp", echo=False)
        # Conecta a la base de datos
        self.connection = engine.connect()
        # Mapea informaci[on de la base de datos
        metadata = db.MetaData()
        # Crea un objeto con la estructura y las propiedades de la tabla personas
        self.empleados = db.Table('Empleado', metadata, autoload=True, autoload_with=engine)
        # Crea un objeto con la estructura y las propiedades de la tabla personas
        self.registros = db.Table('Controlpersonal', metadata, autoload=True, autoload_with=engine)
        # Crea un objeto con la estructura y las propiedades de la tabla registro
        self.registro_mar = db.Table('Control_Marcacion', metadata,autoload=True, autoload_with=engine)
        # Crea un objeto con la estructura y las propiedades de la tabla administradores
        self.administradores = db.Table('administradores', metadata, autoload=True, autoload_with=engine)

    def autenticacion(self, username, password):
        adm_id = self.administradores.c.adm_id
        adm_username = self.administradores.c.adm_username
        adm_password = self.administradores.c.adm_password
        query = db.select([adm_id, adm_username, adm_password]).where(and_(adm_username == username, adm_password == password))
        resultado = self.connection.execute(query)
        ResultSet = list([item for item in resultado.fetchall()])
        if ResultSet == []:
            return False
        else:
            return True

    # Listar todos los empleados
    def listarEmpleado(self, dataframe=False):
        query = db.select([self.registro_mar])
        resultado = self.connection.execute(query)
        ResultSet = resultado.fetchall()
        if dataframe:
            df = pd.DataFrame(ResultSet)
            return df
        else:
            return ResultSet

    # Listar el registro
    def listarRegistro(self, dataframe=False):
        query = db.select([self.registro])
        resultado = self.connection.execute(query)
        ResultSet = resultado.fetchall()
        if dataframe:
            df = pd.DataFrame(ResultSet)
            return df
        else:
            return ResultSet

    # Listar registro con nombre de empleado
    def listarRegistroCruzado(self, dataframe=False):
        idReg = self.registro.c.reg_id
        nombreEmp = self.empleados.c.emp_nombre
        apellidoEmp = self.empleados.c.emp_apellido
        fechaEnt = self.registro.c.reg_fecha_entrada
        horaEnt = self.registro.c.reg_hora_entrada
        fechaSal = self.registro.c.reg_fecha_salida
        horaSal = self.registro.c.reg_hora_salida
        listado = [idReg, nombreEmp, apellidoEmp, fechaEnt, horaEnt, fechaSal, horaSal]
        query = db.select(listado).select_from(self.registro.join(self.empleados)).order_by(self.registro.c.reg_id)
        resultado = self.connection.execute(query)
        ResultSet = resultado.fetchall()
        if dataframe:
            df = pd.DataFrame(ResultSet)
            return df
        else:
            return ResultSet

    # Funcion para marcar entrada
    def marcarEntrada(self, id):
        comp = db.select([self.registro.c.reg_estado]).where(self.registro.c.emp_id == id).order_by(-self.registro.c.reg_id)
        resultado = self.connection.execute(comp)
        ResultSet = [item[0] for item in resultado.fetchall()]
        if ResultSet == [] or ResultSet[0] == 1 or ResultSet[0] == None:
            marcar = db.insert(self.registro).values(reg_fecha_entrada=date.today(), reg_hora_entrada=time.localtime(), emp_id=id, reg_estado=False)
            self.connection.execute(marcar)
            return True
        else:
            return False

    # Funcion para marcar salida
    def marcarSalida(self, id):
        comp = db.select([self.registro.c.reg_estado]).where(self.registro.c.emp_id == id).order_by(-self.registro.c.reg_id)
        resultado = self.connection.execute(comp)
        ResultSet = [item[0] for item in resultado.fetchall()]
        if ResultSet == [] or ResultSet[0] == 1 or ResultSet[0] == None:
            return False
        else:
            marcar = db.update(self.registro).values(reg_fecha_salida=date.today(), reg_hora_salida=time.localtime(), reg_estado=True).where(and_(self.registro.c.emp_id == id, self.registro.c.reg_hora_salida == time.time()))
            self.connection.execute(marcar)
            return True

    # Inserta una persona al registro
    def crearEmpleado(self, datosEmpleado):
        insertarPersona = db.insert(self.empleados).values(datosEmpleado)
        self.connection.execute(insertarPersona)

    # Funcion para actualizar parametros de la persona
    def actualizarEmpleado(self, empleado, cedula):
        actualizarPersona = db.update(self.empleados).values(empleado).where(self.empleados.c.emp_cedula == cedula)
        self.connection.execute(actualizarPersona)

    def actualizarRegistro(self, registro, id_registro):
        actualizarRegistro = db.update(self.registro).values(registro).where(self.registro.c.reg_id == id_registro)
        self.connection.execute(actualizarRegistro)

    def buscarID(self, cedula):
        buscarID = db.select([self.empleados.c.emp_id]).where(self.empleados.c.emp_cedula == cedula)
        resultado = self.connection.execute(buscarID)
        ResultSet = [item[0] for item in resultado.fetchall()]
        if ResultSet == []:
            return None
        else:
            return ResultSet[0]

    def imprimirQuery(self, entrada):
        print("entrada", entrada)

"""conectarbd = Conexion()
resultado = conectarbd.listarEmpleado(dataframe=True)
conectarbd.imprimirQuery(resultado)"""