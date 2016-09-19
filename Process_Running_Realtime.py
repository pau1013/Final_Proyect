import os

finished=False
def Process_Running(finished):
    while finished==False:

        actualizar= input("Deseas actualizar los procesos? (Y) | (N)")
        if (str(actualizar)).upper()=="Y":
            process_output=os.popen("ps -Af").read()
            print(process_output)
        else:
            finished=True

#Commit de Prueba para tarea


Process_Running(finished)
