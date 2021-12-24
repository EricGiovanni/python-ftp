import socket
import sys
import os
import struct


ip = "127.0.0.1"
port = 1234
buffer = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def recibir_archivo(filename):
    with open(filename, "wb") as f:
        sock.send(b"ready")
        while True:
            data = sock.recv(buffer)
            print(data)
            if not data:
                print("Archivo recibido")
                return
            f.write(data)


def ls():
    print("Listando archivos...")
    try:
        sock.send(b"1")
    except:
        print("No se pudo enviar la instrucción")
        return
    try:
        files = sock.recv(buffer)
        print("------------------------")
        print(files.decode("utf-8"))
        print("------------------------")
    except:
        print("No se pudo recibir la lista de archivos")
    try:
        sock.send(b"success")
        return
    except:
        print("No se obtuvo confirmacion del servidor")
        return


def rm():
    try:
        sock.send(b"2")
    except:
        print("No se pudo enviar la instrucción")
        return
    try:
        msg = sock.recv(buffer)
        print("------------------------")
        print(msg.decode("utf-8"))
        print("------------------------")
        file_rm = input("Ingrese el nombre del archivo a eliminar: ")
        sock.send(bytes(file_rm, encoding="utf-8"))
        msg = sock.recv(buffer)
        print("------------------------")
        print(msg.decode("utf-8"))
        print("------------------------")
    except:
        print("No se pudo realizar la operación")


def actualizar():
    try:
        sock.send(b"3")
    except:
        print("No se pudo enviar la instrucción")
        return
    try:
        msg = sock.recv(buffer)
        print("------------------------")
        print(msg.decode("utf-8"))
        print("------------------------")
        file_upd = input("Ingrese el nombre del archivo a actualizar: ")
        sock.send(bytes(file_upd, encoding="utf-8"))
        msg = sock.recv(buffer)
        print("------------------------")
        print(msg.decode("utf-8"))
        print("------------------------")
        if msg.decode("utf-8") == "No se pudo actualizar el archivo" or msg.decode("utf-8") == "No existe el archivo":
            return
        file_upd = input("Ingrese el nuevo nombre del archivo: ")
        sock.send(bytes(file_upd, encoding="utf-8"))
        msg = sock.recv(buffer)
        print("------------------------")
        print(msg.decode("utf-8"))
        print("------------------------")
    except:
        print("No se pudo realizar la operación")


def descargar():
    try:
        sock.send(b"4")
    except:
        print("No se pudo enviar la instrucción")
        return
    try:
        msg = sock.recv(buffer)
        print("------------------------")
        print(msg.decode("utf-8"))
        print("------------------------")
        file_dwn = input("Ingrese el nombre del archivo a descargar: ")
        sock.send(bytes(file_dwn, encoding="utf-8"))
        msg = sock.recv(buffer)
        print("------------------------")
        print(msg.decode("utf-8"))
        print("------------------------")
        print("Recibiendo archivo...")
        print("------------------------")
        if msg.decode("utf-8") == "Enviando archivo...":
            recibir_archivo(file_dwn)
            print("------------------------")
            print("Debes presionar ctrl + c para terminar de recibir el archivo")
            print("------------------------")
    except:
        print("No se pudo realizar la operación")


def subir():
    try:
        sock.send(b"5")
    except:
        print("No se pudo enviar la instrucción")
        return
    try:
        msg = sock.recv(buffer)
        print("------------------------")
        print(msg.decode("utf-8"))
        print("------------------------")
        file_upl = input("Ingrese el nombre del archivo a subir: ")
        if os.path.isfile(file_upl):
            sock.send(bytes(file_upl, encoding="utf-8"))
            msg = sock.recv(buffer)
            print("------------------------")
            print(msg.decode("utf-8"))
            print("------------------------")
            print("Enviando archivo...")
            print("------------------------")
            with open(file_upl, "rb") as f:
                data = f.read(buffer)
                while data:
                    sock.sendall(data)
                    data = f.read(buffer)
            print("------------------------")
            print("Debes presionar ctrl + c para terminar de recibir el archivo")
            print("------------------------")
            print("Archivo enviado correctamente")
            return
        else:
            print("El archivo no existe")
            sock.send(b"No existe el archivo")
            msg = sock.recv(buffer)
            print("------------------------")
            print(msg.decode("utf-8"))
            print("------------------------")
            return
    except:
        print("No se pudo realizar la operación")


if __name__ == "__main__":
    print("Iniciando cliente...")
    try:
        sock.connect((ip, port))
        print("Conexión establecida con el servidor...")
    except:
        print("No se pudo establecer conexión con el servidor...")
        sys.exit(-1)
    while True:
        print("Bienvenido al servidor FTP")
        print("¿Qué deseas hacer?")
        print("1. Listar archivos")
        print("2. Borrar archivo")
        print("3. Actualizar archivo")
        print("4. Descargar archivo")
        print("5. Subir archivo")
        print("6. Ayuda")
        print("7. Salir")
        entrada = input("Ingrese una opción: ")
        if entrada == "1":
            ls()
        elif entrada == "2":
            rm()
        elif entrada == "3":
            actualizar()
        elif entrada == "4":
            descargar()
        elif entrada == "5":
            subir()
        elif entrada == "6":
            print("1. Listar archivos -- Lista los archivos del servidor")
            print("2. Borrar archivo -- Borra un archivo del servidor")
            print("3. Actualizar archivo -- Actualiza un archivo del servidor")
            print(
                "4. Descargar archivo -- Descarga un archivo del servidor (Solo pueden ser archivos de texto)")
            print(
                "5. Subir archivo -- Subir un archivo al servidor (Solo pueden ser archivos de texto)")
        elif entrada == "7":
            print("Cerrando conexión...")
            sock.send(b"7")
            sock.close()
            break
        else:
            print("Opción inválida")
