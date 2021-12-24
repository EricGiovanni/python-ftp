import socket
import sys
import time
import os
import struct

print("Iniciando servidor...")
ip = "127.0.0.1"
port = 1234
buffer = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, port))
sock.listen(1)
conn, addr = sock.accept()


def enviar_archivo(filename):
    print(conn.recv(buffer).decode("utf-8"))
    with open(filename, "rb") as f:
        data = f.read(buffer)
        while data:
            conn.sendall(data)
            data = f.read(buffer)
    print("Archivo enviado correctamente")


def recibir_archivo(filename):
    with open(filename, "wb") as f:
        conn.send(b"ready")
        while True:
            data = conn.recv(buffer)
            if not data:
                print("Archivo recibido")
                break
            f.write(data)


def ls():
    print("Listando archivos...")
    files = os.listdir(os.getcwd())
    files.remove("servidor.py")
    files = bytes(
        '\n'.join(files), encoding="utf-8")
    conn.send(files)
    conn.recv(buffer)
    print("Se envio la lista de archivos correctamente")


def rm():
    conn.send(b"Que archivo deseas eliminar?")
    file_rm = conn.recv(buffer).decode("utf-8")
    if file_rm == "servidor.py":
        conn.send(b"No se puede eliminar este archivo")
        return
    if os.path.isfile(file_rm):
        os.remove(file_rm)
        conn.send(b"Archivo eliminado")
    else:
        conn.send(b"No existe el archivo")


def actualizar():
    conn.send(b"Que archivo deseas actualizar?")
    file_upd = conn.recv(buffer).decode("utf-8")
    if file_upd == "servidor.py":
        conn.send(b"No se puede actualizar este archivo")
        return
    if os.path.isfile(file_upd):
        conn.send(b"Archivo encontrado. Ingrese el nuevo nombre:")
        new_name = conn.recv(buffer).decode("utf-8")
        os.rename(file_upd, new_name)
        conn.send(b"Archivo actualizado")
    else:
        conn.send(b"No existe el archivo")


def descargar():
    conn.send(b"Que archivo deseas descargar?")
    file_dwn = conn.recv(buffer).decode("utf-8")
    if file_dwn == "servidor.py":
        conn.send(b"No se puede descargar este archivo")
        return
    if os.path.isfile(file_dwn):
        print("Enviando archivo...")
        conn.send(b"Enviando archivo...")
        enviar_archivo(file_dwn)
    else:
        conn.send(b"No existe el archivo")


def subir():
    conn.send(b"Que archivo deseas subir?")
    file_upl = conn.recv(buffer).decode("utf-8")
    if file_upl == "servidor.py" or file_upl == "No existe el archivo":
        conn.send(
            b"No se puede subir un archivo con ese nombre o el archivo no existe")
        return
    if os.path.isfile(file_upl):
        print("El archivo se sobreescribira...")
        conn.send(b"El archivo se sobreescribira...")
        recibir_archivo(file_upl)
    else:
        conn.send(b"Se creara el nuevo archivo")
        recibir_archivo(file_upl)


if __name__ == "__main__":
    while True:
        print("Esperando acción a realizar...")
        data = conn.recv(buffer)
        print("Instrucción a realizar:", data)
        if data == b"1":
            ls()
        elif data == b"2":
            rm()
        elif data == b"3":
            actualizar()
        elif data == b"4":
            descargar()
        elif data == b"5":
            subir()
        elif data == b"7":
            print("Cerrando conexión...")
            conn.close()
            break
