from datetime import datetime,time


hora_entrada_inicial = time(7,0,0,0)
hora_entrada_final = time(10,0,0,0)
hora_marcacion = time(7,15,0,0) 
id_persona = 3
#mar_estado = Controlpersonal.objects.get(id = id_persona)
#marcacion_entrada = .mar_estado
#Controlpersonal.objects.get(id=1).mar_estado




if hora_entrada_inicial <= hora_marcacion and hora_entrada_final >= hora_marcacion:
    print("MARCACION ACEPTADA")
    #Controlpersonal.objects.filter(id=id_persona).update(mar_estado = 1)

elif hora_entrada_inicial >= hora_marcacion:
    print("ESPERE SE HABILITA EL SISTEMA")

elif hora_entrada_final < hora_marcacion:
    print("LLEGA TARDE")


